import os
import re
import json

input_dir = "../data/clean"
output_dir = "../data/chunks"
os.makedirs(output_dir, exist_ok=True)

def parse_markdown_sections(file_path, title):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match top-level metadata (optional)
    main_title_match = re.match(r"# (.+)", content)
    main_title = main_title_match.group(1).strip() if main_title_match else title

    # Split by level-2 headings
    sections_raw = re.split(r"(## .+)", content)
    sections = []
    current_heading = None
    current_content = []

    for block in sections_raw:
        if block.startswith("## "):
            if current_heading and current_content:
                text = "".join(current_content).strip()
                if len(text) > 30:
                    sections.append({
                        "heading": current_heading,
                        "content": text,
                        "tokens": len(text.split())
                    })
            current_heading = block.strip()
            current_content = []
        else:
            current_content.append(block)

    # Final section
    if current_heading and current_content:
        text = "".join(current_content).strip()
        if len(text) > 30:
            sections.append({
                "heading": current_heading,
                "content": text,
                "tokens": len(text.split())
            })

    # Full chunk
    return {
        "title": main_title,
        "heading": f"# {main_title}",
        "sections": sections,
        "tokens": sum(section["tokens"] for section in sections)
    }

# Process all markdown files
for filename in os.listdir(input_dir):
    if filename.endswith(".md"):
        file_path = os.path.join(input_dir, filename)
        title = filename.replace(".md", "")
        chunk = parse_markdown_sections(file_path, title)

        output_path = os.path.join(output_dir, title + ".jsonl")
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(chunk, out)
            out.write("\n")

print("✅ All markdown files chunked with nested sections in ../data/chunks/")
