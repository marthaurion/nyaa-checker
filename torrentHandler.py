import tomllib
from qbittorrentapi import Client

CONFIG_FILE = "config/config.toml"

def loadConfig() -> tuple[str, int, str, str]:
    with open(CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)
        qbHost = config["qbittorrent"]["host"]
        qbPort = config["qbittorrent"]["port"]
        qbUser = config["qbittorrent"]["username"]
        qbPass = config["qbittorrent"]["password"]
        if not qbHost or not qbPort or not qbUser or not qbPass:
            raise ValueError("Invalid or missing qBittorrent configuration in config.toml")
        return qbHost, qbPort, qbUser, qbPass

class QBHandler():
    def __init__(self):
        qbHost, qbPort, qbUser, qbPass = loadConfig()
        self.qb = Client(
                host=qbHost,
                port=qbPort,
                username=qbUser,
                password=qbPass
            )
    
    def addToQB(self, magnet_url: str, title: str):
        print(f"  → Adding to qBittorrent: {title}")
        self.qb.torrents_add(urls=magnet_url)