import os
import re

RAW_DIR = "../data/raw/text"
CLEANED_DIR = "../data/cleaned"

NOISE_PATTERNS = [
    r"Home\s*>.*",                 # breadcrumb menus
    r"Admissions\s*>.*",
    r"Back to top",
    r"© National University.*",
    r"Last updated.*",
    r"Privacy Policy",
    r"Terms & Conditions",
    r"Rohtas Road, G-9/4",
    r"Islamabad - 44000"
]

def clean_text(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line: continue

        # Skip noise
        if any(re.search(pat, line, re.IGNORECASE) for pat in NOISE_PATTERNS):
            continue

        # Normalize spacing
        line = re.sub(r"\s+", " ", line)
        cleaned.append(line)

    return "\n".join(cleaned)

def main():
    os.makedirs(CLEANED_DIR, exist_ok=True)
    for filename in os.listdir(RAW_DIR):
        if not filename.endswith(".txt"):
            continue

        raw_path = os.path.join(RAW_DIR, filename)
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned_text = clean_text(raw_text)

        cleaned_path = os.path.join(CLEANED_DIR, filename)
        with open(cleaned_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"Cleaned {filename}")

if __name__ == "__main__":
    main()