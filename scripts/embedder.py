from sentence_transformers import SentenceTransformer
import chromadb
import json
import os
from tqdm import tqdm

# === Paths ===
data_dir = "../data/chunks"
db_dir = "../data/vector_store"
os.makedirs(db_dir, exist_ok=True)

# === Initialize Persistent ChromaDB ===
chroma_client = chromadb.PersistentClient(path=db_dir)
collection = chroma_client.get_or_create_collection(name="fast_chunks")

# === Load embedding model ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# === Collect data ===
documents, metadatas, ids = [], [], []
doc_id = 0

for file in os.listdir(data_dir):
    if file.endswith(".jsonl"):
        with open(os.path.join(data_dir, file), "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                content = record["content"].strip()
                if not content:
                    continue
                documents.append(content)
                metadatas.append({
                    "title": record.get("title", ""),
                    "heading": record.get("heading", "")
                })
                ids.append(str(doc_id))
                doc_id += 1

# === Batch embedding and storage ===
batch_size = 32
for i in tqdm(range(0, len(documents), batch_size)):
    batch_docs = documents[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]
    batch_meta = metadatas[i:i+batch_size]

    embeddings = model.encode(
        batch_docs,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).tolist()

    collection.add(
        documents=batch_docs,
        metadatas=batch_meta,
        ids=batch_ids,
        embeddings=embeddings
    )

print(f"✅ All chunks embedded and stored in persistent vector DB at: {db_dir}")
