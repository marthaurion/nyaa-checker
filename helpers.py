import tomllib
from pathlib import Path

CONFIG_FILE = Path("config") / "config.toml"

def loadQBConfig() -> tuple[str, int, str, str]:
    with open(CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)
        qbHost = config["qbittorrent"]["host"]
        qbPort = config["qbittorrent"]["port"]
        qbUser = config["qbittorrent"]["username"]
        qbPass = config["qbittorrent"]["password"]
        if not qbHost or not qbPort or not qbUser or not qbPass:
            raise ValueError("Invalid or missing qBittorrent configuration in config.toml")
        return qbHost, qbPort, qbUser, qbPass

def getNyaaStartPage() -> int:
    with open(CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)
        return config["nyaa"].get("startPage", 1)