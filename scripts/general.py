import requests
from bs4 import BeautifulSoup
import os

# Pages to scrape
pages = {
    "calendar": "https://www.nu.edu.pk/Student/Calender",
    "conduct": "https://www.nu.edu.pk/Student/Conduct",
    "grading": "https://www.nu.edu.pk/Student/Grading",
    "finacialRules": "https://www.nu.edu.pk/Student/FinancialRules",
    "programs": "https://www.nu.edu.pk/Degree-Programs",
    "howToApply": "https://www.nu.edu.pk/Admissions/HowToApply",
    "eligibility": "https://www.nu.edu.pk/Admissions/EligibilityCriteria",
    "scholarships": "https://www.nu.edu.pk/Admissions/Scholarship",
    "testPattern": "https://www.nu.edu.pk/Admissions/TestPattern",
    "feeStructure": "https://www.nu.edu.pk/Admissions/FeeStructure",
    "FAQs": "https://www.nu.edu.pk/Admissions/FAQ"

}

# Create directories
os.makedirs("../data/raw/html", exist_ok=True)
os.makedirs("../data/raw/text", exist_ok=True)


def extract_page(name, url):
    response = requests.get(url)

    # Save raw HTML
    html_path = f"../data/raw/html/{name}.html"
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
    text_path = f"../data/raw/text/{name}.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Saved {name}: HTML → {html_path}, Text → {text_path}")


# Scrape each page
for name, url in pages.items():
    extract_page(name, url)

print("✅ All pages scraped and saved (HTML + Text)!")
