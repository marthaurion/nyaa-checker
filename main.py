import sys
import argparse
import logging
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from lnTracker import LNTracker
from torrentHandler import QBHandler
from helpers import getNyaaStartPage

# -------------------
# CONFIG
# -------------------
SEARCH_URL = "https://nyaa.si/"
CATEGORY = "3_1" # English-Translated Light Novels

KEYWORDS = ["[Yen Press]", "[J-Novel Club]", "[Seven Seas]", "[Kobo]", "[Kindle]", "[Kadokawa]", "[Cross Infinite World]"]
INCREMENTAL_PAGES = 3
MAX_PAGES = 20

def scrapeSinglePage(page: int) -> list[tuple[str, str, str]]:
    url = SEARCH_URL + f"?c={CATEGORY}" + f"&p={page}"
    logging.info(f"Scraping page {page}: {url}")
    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        logging.error(f"Failed to fetch page {page}, status code: {resp.status_code}")
        logging.error(resp.text)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    rows = soup.select("table.torrent-list tbody tr")

    results = []
    for row in rows:
        # Title is in column 2
        titleElem = row.select_one("td:nth-of-type(2) a:not(.comments)")
        if not titleElem:
            continue
        title = str(titleElem.text).strip()
        viewLink = str(titleElem["href"])
        torrentID = viewLink.replace("/view/", "")

        # Magnet link is in column 3
        magnetElem = row.select_one("td:nth-of-type(3) a[href^='magnet:']")
        if not magnetElem:
            continue
        magnet = str(magnetElem["href"])

        results.append((torrentID, title, magnet))

    return results

def scrapePages(max_pages: int = MAX_PAGES):
    qb = QBHandler()
    tracker = LNTracker()
    logPath = Path("logs") / "output.log"
    logPath.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=logPath, filemode="w", level=logging.INFO)
    startPage = getNyaaStartPage()

    for page in range(startPage, max_pages + 1):
        results = scrapeSinglePage(page)
        if not results:
            break

        for torrentID, title, magnet in results:
            if torrentID and not tracker.isNew(torrentID):
                continue
            if not any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                continue
            
            logging.info(f"{title}\n{torrentID}\n{magnet}\n")
            qb.addToQB(magnet, title)
            tracker.markSeen(torrentID, title)


# -------------------
# CLI Entry
# -------------------
def main():
    parser = argparse.ArgumentParser(description="Light Novel Downloader for Nyaa")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["incremental", "historical"],
        help="Run mode (incremental=page 1, historical=crawl old pages)",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=MAX_PAGES,
        help="Max pages to crawl in historical mode (default: 20)",
    )

    args = parser.parse_args()

    if args.mode == "incremental" or len(sys.argv) == 1:
        scrapePages(max_pages=INCREMENTAL_PAGES)
    elif args.mode == "historical":
        scrapePages(max_pages=args.pages)


if __name__ == "__main__":
    main()