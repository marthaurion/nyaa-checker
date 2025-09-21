import logging
from pathlib import Path
from qbittorrentapi import Client
from helpers import loadQBConfig

SAVE_PATH = Path("E:/Downloads") / "Light Novels"

class QBHandler():
    def __init__(self):
        qbHost, qbPort, qbUser, qbPass = loadQBConfig()
        self.qb = Client(
                host=qbHost,
                port=qbPort,
                username=qbUser,
                password=qbPass
            )
    
    def addToQB(self, magnet_url: str, title: str):
        logging.info(f"Adding to qBittorrent: {title}")
        self.qb.torrents_add(urls=magnet_url, save_path=str(SAVE_PATH))