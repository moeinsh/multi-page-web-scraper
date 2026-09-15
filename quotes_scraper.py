"""Sample project: multi-page web scraper (BeautifulSoup).

Scrapes all pages of the public demo site quotes.toscrape.com,
extracts quote text, author and tags, and saves everything to CSV.
Demonstrates: pagination handling, CSS selectors, data cleaning,
CSV export with UTF-8 encoding.
"""
import csv

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio-sample)"}


def scrape_all_quotes():
    quotes = []
    url = BASE_URL
    session = requests.Session()
    session.headers.update(HEADERS)

    while url:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for box in soup.select("div.quote"):
            text = box.select_one("span.text").get_text(strip=True)
            author = box.select_one("small.author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in box.select("div.tags a.tag")]
            quotes.append({"quote": text, "author": author, "tags": ";".join(tags)})

        nxt = soup.select_one("li.next > a")
        url = BASE_URL + nxt["href"] if nxt else None

    return quotes


def main():
    quotes = scrape_all_quotes()
    with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"])
        writer.writeheader()
        writer.writerows(quotes)
    authors = {q["author"] for q in quotes}
    print(f"Scraped {len(quotes)} quotes from {len(authors)} authors -> quotes.csv")


if __name__ == "__main__":
    main()
