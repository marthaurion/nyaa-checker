import sqlite3
from pathlib import Path

DB_FILE = Path("db") / "nyaa_ln.db"

class LNTracker():
    def __init__(self):
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(DB_FILE))
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS seen (guid TEXT PRIMARY KEY, title TEXT)")
        self.conn.commit()
    
    def isNew(self, guid: str) -> bool:
        self.cur.execute("SELECT 1 FROM seen WHERE guid=?", (guid,))
        return self.cur.fetchone() is None
    
    def markSeen(self, guid: str, title: str):
        self.cur.execute("INSERT OR IGNORE INTO seen (guid, title) VALUES (?, ?)", (guid, title))
        self.conn.commit()