import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# Constants
RSS_FEED_URL = "https://nyaa.si/?page=rss&c=3_1"
DOWNLOAD_FOLDER = Path("E:/Downloads") / "LN Folder"
TRACKED_TORRENTS_FILE = DOWNLOAD_FOLDER / "downloaded_torrents.txt"
KEYWORDS = ["[Yen Press]", "[J-Novel Club]", "[Seven Seas]", "[Kobo]", "[Kindle]", "[Kadokawa]"]

# Ensure download folder exists
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

def load_downloaded_torrents():
    """Load the list of already downloaded torrents to avoid duplicates."""
    if TRACKED_TORRENTS_FILE.exists():
        return set(TRACKED_TORRENTS_FILE.read_text().splitlines())
    return set()

def save_downloaded_torrent(torrent_id):
    """Save a new torrent ID to the tracking file."""
    with TRACKED_TORRENTS_FILE.open("a") as f:
        f.write(torrent_id + "\n")

def fetch_light_novels():
    """Fetch new light novel torrents from the Nyaa.si RSS feed."""
    print(f"[{datetime.now()}] Fetching torrents from RSS feed...")
    downloaded_torrents = load_downloaded_torrents()
    new_torrents_found = 0

    response = requests.get(RSS_FEED_URL)
    if response.status_code != 200:
        print(f"Failed to fetch RSS feed, status code: {response.status_code}")
        return

    root = ET.fromstring(response.content)
    
    for item in root.findall(".//item"):
        title = item.find("title").text
        magnet_link = item.find("link").text
        torrent_id = magnet_link.split("&")[0]  # Unique identifier from magnet hash

        # Skip already downloaded torrents
        #if torrent_id in downloaded_torrents:
        #    continue

        # Filter by keywords
        if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
            print(f"New light novel found: {title}")
            print(magnet_link)
            #save_magnet_link(magnet_link, title)
            #save_downloaded_torrent(torrent_id)
            new_torrents_found += 1

    if new_torrents_found == 0:
        print("No new torrents found.")

def save_magnet_link(magnet_link, title):
    """Save the magnet link to a text file."""
    magnet_file = DOWNLOAD_FOLDER / "magnet_links.txt"
    with magnet_file.open("a") as f:
        f.write(f"{title}\n{magnet_link}\n\n")
    print(f"Saved magnet link for: {title}")

if __name__ == "__main__":
    fetch_light_novels()