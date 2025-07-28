import requests
from bs4 import BeautifulSoup
import os

# Pages to scrape
pages = {
    "BBA": "https://www.nu.edu.pk/Program/BBA",
    "BS(AF)": "https://www.nu.edu.pk/Program/BS(AF)",
    "BS(AI)": "https://www.nu.edu.pk/Program/BS(AI)",
    "BS(BA)": "https://www.nu.edu.pk/Program/BS(BA)",
    "BS(CV)": "https://www.nu.edu.pk/Program/BS(CV)",
    "BS(CE)": "https://www.nu.edu.pk/Program/BS(CE)",
    "BS(CS)": "https://www.nu.edu.pk/Program/BS(CS)",
    "BS(CY)": "https://www.nu.edu.pk/Program/BS(CY)",
    "BS(DS)": "https://www.nu.edu.pk/Program/BS(DS)",
    "BS(EE)": "https://www.nu.edu.pk/Program/BS(EE)",
    "BS(FT)": "https://www.nu.edu.pk/Program/BS(FinTech)",
    "BS(SE)": "https://www.nu.edu.pk/Program/BS(SE)",
    "MBA": "https://www.nu.edu.pk/Program/MBA",
    "MS(LING)": "https://www.nu.edu.pk/Program/MS(LING)",
    "MS(AI)": "https://www.nu.edu.pk/Program/MS(AI)",
    "MS(BA)": "https://www.nu.edu.pk/Program/MS(BA)",
    "MS(CV)": "https://www.nu.edu.pk/Program/MS(CV)",
    "MS(CS)": "https://www.nu.edu.pk/Program/MS(CS)",
    "MS(DS)": "https://www.nu.edu.pk/Program/MS(DS)",
    "MS(EE)": "https://www.nu.edu.pk/Program/MS(EE)",
    "MS(Math)": "https://www.nu.edu.pk/Program/MS(Math)",
    "MS(SE)": "https://www.nu.edu.pk/Program/MS(SE)",
    "MS(SPM)": "https://www.nu.edu.pk/Program/MS(SPM)",
    "PhD(CV)": "https://www.nu.edu.pk/Program/PhD(CV)",
    "PhD(CS)": "https://www.nu.edu.pk/Program/PhD(CS)",
    "PhD(EE)": "https://www.nu.edu.pk/Program/PhD(EE)",
    "PhD(MS)": "https://www.nu.edu.pk/Program/PhD(MS)",
    "PhD(Math)": "https://www.nu.edu.pk/Program/PhD(Math)",
    "PhD(SE)": "https://www.nu.edu.pk/Program/PhD(SE)",
    "Phd(EngLING)": "https://www.nu.edu.pk/Program/PhD(SE)"
}

# Create directories
os.makedirs("../data/raw/html/programs", exist_ok=True)
os.makedirs("../data/raw/text/programs", exist_ok=True)


def extract_page(name, url):
    response = requests.get(url)

    # Save raw HTML
    html_path = f"../data/raw/html/programs/{name}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract headings
    headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]

    # Extract paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

    # Extract tables in Markdown format
    tables = []
    for table in soup.find_all('table'):
        rows = []
        for tr in table.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            if cells:
                rows.append("| " + " | ".join(cells) + " |")
        if rows:
            tables.append("\n".join(rows))

    # Combine content
    content = "\n\n".join(headings + paragraphs + tables)

    # Save text file
    text_path = f"../data/raw/text/programs/{name}.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Saved {name}: HTML → {html_path}, Text → {text_path}")


# Scrape each page
for name, url in pages.items():
    extract_page(name, url)

print("✅ All pages scraped and saved (HTML + Text)!")
