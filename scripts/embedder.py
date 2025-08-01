from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import json
from tqdm import tqdm

import shutil


# === Paths ===
data_dir = "../data/chunks"
CHROMA_PATH = "../data/vector_store"
os.makedirs(CHROMA_PATH, exist_ok=True)

shutil.rmtree(CHROMA_PATH, ignore_errors=True)

# === Load embedding model ===
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# === Collect text chunks and metadata ===
texts, metadatas = [], []

for file in os.listdir(data_dir):
    if file.endswith(".jsonl"):
        with open(os.path.join(data_dir, file), "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)

                title = record.get("title", "")
                heading = record.get("heading", "")
                sections = record.get("sections", [])

                for section in sections:
                    content = section.get("content", "").strip()
                    if content:
                        texts.append(content)
                        metadatas.append({
                            "title": title,
                            "file_heading": heading,
                            "section_heading": section.get("heading", "")
                        })

# === Sanity check
if not texts:
    print("❌ No content found for embedding. Check your input files.")
    exit()

# === Embed and persist to Chroma ===
print(f"📄 Embedding {len(texts)} sections...")
vectorstore = Chroma.from_texts(
    texts=texts,
    embedding=embedding_model,
    metadatas=metadatas,
    persist_directory=CHROMA_PATH
)

vectorstore.persist()  # Safe for older LangChain versions

print(f"✅ Successfully embedded and stored {len(texts)} sections.")
