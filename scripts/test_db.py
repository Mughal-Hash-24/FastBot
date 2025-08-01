import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables
load_dotenv()

# === Configuration ===
CHROMA_PATH = "../data/vector_store"
EMBED_MODEL = "all-MiniLM-L6-v2"

# === Initialize embedding model ===
embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

# === Resolve path and debug
resolved_path = os.path.abspath(CHROMA_PATH)
print(f"🔍 Checking vector store at: {resolved_path}")

# === Load Chroma DB
vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model
)

# === Fetch and display some docs
db = vector_store.get()
documents = db.get("documents", [])
metadatas = db.get("metadatas", [])

print(f"\n✅ Loaded vector store. Total documents: {len(documents)}")

# Preview first few entries
preview_count = min(100000, len(documents))
print(f"\n🔎 Showing first {preview_count} document(s):\n")

for i in range(preview_count):
    print(f"--- Document {i+1} ---")
    print("Content:")
    print(documents[i])
    if i < len(metadatas):
        print("\nMetadata:")
        print(metadatas[i])
    print("\n" + "-"*40 + "\n")
