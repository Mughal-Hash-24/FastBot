import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

# === Load environment variables ===
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_PATH = "data/vector_store"
EMBED_MODEL = "all-MiniLM-L6-v2"

# === Setup Logging ===
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/fastbot.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("🚀 Starting FASTBot server...")

# === Initialize FastAPI app ===
app = FastAPI()

# === CORS Configuration ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  # Add OPTIONS explicitly
    allow_headers=["*"],
)

# === Request body schema ===
class QueryRequest(BaseModel):
    query: str

# === Load embedding model and vector store ===
embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
vector_store = Chroma(
    persist_directory=os.path.abspath(CHROMA_PATH),
    embedding_function=embedding_model
)
retriever = vector_store.as_retriever()

doc_count = len(vector_store.get().get("documents", []))
logging.info(f"📚 Loaded vector store with {doc_count} documents.")

# === Initialize LLM ===
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192",
    temperature=0.2
)

# === Create RAG Chain ===
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# === Routes ===
@app.post("/chat")
async def chat(req: QueryRequest):
    logging.info(f"📥 Query received: {req.query}")

    docs = retriever.get_relevant_documents(req.query)
    logging.info(f"🔍 Retrieved {len(docs)} relevant document(s).")

    response = qa_chain.invoke(req.query)
    answer = response.get("result", "")
    logging.info(f"✅ Answer generated. Length: {len(answer)} characters.")

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in response.get("source_documents", [])]
    }

@app.get("/")
def root():
    return {"message": "FASTBot backend is running with Groq + LangChain 🚀"}
