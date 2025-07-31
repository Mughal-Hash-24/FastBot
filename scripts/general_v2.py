import os
from bs4 import BeautifulSoup

raw_dir = "../data/raw/html/programs"
output_dir = "../data/clean/programs"
os.makedirs(output_dir, exist_ok=True)

def is_garbage_list(tag):
    # Reject lists inside nav, header, footer, or similar semantic containers
    blacklist = ['nav', 'header', 'footer', 'menu', 'breadcrumb']
    parent = tag.find_parent()
    while parent:
        if parent.name in blacklist or any(cls in blacklist for cls in parent.get("class", [])):
            return True
        parent = parent.find_parent()
    return False

def extract_structured_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    content = []

    for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'table', 'ul', 'ol']):
        if tag.name.startswith('h'):
            level = int(tag.name[1])
            content.append(f"{'#' * level} {tag.get_text(strip=True)}")

        elif tag.name == 'p':
            text = tag.get_text(strip=True)
            if text:
                content.append(text)

        elif tag.name == 'table':
            rows = []
            for tr in tag.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)

            if rows:
                header = rows[0]
                table = [
                    "| " + " | ".join(header) + " |",
                    "| " + " | ".join([":--" for _ in header]) + " |"
                ]
                for row in rows[1:]:
                    table.append("| " + " | ".join(row) + " |")
                content.append("\n".join(table))

        elif tag.name in ['ul', 'ol'] and not is_garbage_list(tag):
            items = []
            for i, li in enumerate(tag.find_all('li'), 1):
                text = li.get_text(strip=True)
                if text:
                    if tag.name == 'ul':
                        items.append(f"- {text}")
                    else:
                        items.append(f"{i}. {text}")
            if items:
                content.append("\n".join(items))

    return "\n\n".join(content)

# Run over all HTML files
for file_name in os.listdir(raw_dir):
    if file_name.endswith(".html"):
        input_path = os.path.join(raw_dir, file_name)
        output_path = os.path.join(output_dir, file_name.replace(".html", ".md"))
        structured_text = extract_structured_text(input_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(structured_text)

print("✅ Markdown files with headings, clean tables, and lists (ul/ol) saved in ../data/clean/programs")
