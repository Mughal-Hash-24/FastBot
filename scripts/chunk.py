import os
import re
import json

input_dir = "../data/clean/programs"
output_dir = "../data/chunks/programs"
os.makedirs(output_dir, exist_ok=True)

def chunk_markdown(file_path, title):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by second-level heading
    blocks = re.split(r"(## .+)", content)

    chunks = []
    current_heading = None
    current_content = []

    for block in blocks:
        if block.startswith("## "):
            if current_heading and current_content:
                text = "".join(current_content).strip()
                if len(text) > 30:
                    chunks.append({
                        "title": title,
                        "heading": current_heading,
                        "content": text,
                        "tokens": len(text.split())  # rough token estimate
                    })
            current_heading = block.strip()
            current_content = []
        else:
            current_content.append(block)

    # Final chunk
    if current_heading and current_content:
        text = "".join(current_content).strip()
        if len(text) > 30:
            chunks.append({
                "title": title,
                "heading": current_heading,
                "content": text,
                "tokens": len(text.split())
            })

    return chunks

# Process each markdown file
for filename in os.listdir(input_dir):
    if filename.endswith(".md"):
        file_path = os.path.join(input_dir, filename)
        title = filename.replace(".md", "")
        chunks = chunk_markdown(file_path, title)

        output_path = os.path.join(output_dir, title + ".jsonl")
        with open(output_path, "w", encoding="utf-8") as out:
            for chunk in chunks:
                json.dump(chunk, out)
                out.write("\n")

print("✅ Markdown files chunked and saved to ../data/chunks/")
