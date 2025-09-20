import sqlite3
DB_FILE = "nyaa_ln.db"

class LNTracker():
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS seen (guid TEXT PRIMARY KEY)")
        self.conn.commit()
    
    def isNew(self, guid: str) -> bool:
        self.cur.execute("SELECT 1 FROM seen WHERE guid=?", (guid,))
        return self.cur.fetchone() is None
    
    def markSeen(self, guid: str):
        self.cur.execute("INSERT OR IGNORE INTO seen (guid) VALUES (?)", (guid,))
        self.conn.commit()