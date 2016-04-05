import os
import sqlite3
from .store import Store


class SQLiteStore(Store):
    """
    A key-value store backed by a SQLite database.
    """

    def __init__(self, storepath):
        if storepath == ":memory:":
            is_new = True
        else:
            is_new = not os.path.exists(storepath)
        
        self.db = sqlite3.connect(storepath, isolation_level="IMMEDIATE")
        self.db.execute("PRAGMA journal_mode=WAL")
        
        if is_new:
            self.db.execute("CREATE TABLE kvs (key VARCHAR(255) NOT NULL PRIMARY KEY, value TEXT)")
            self.db.commit()
    
    def __enter__(self):
        return self

    def __exit__(self, rtype, rvalue, rtraceback):
        if rtype is None:
            self.db.commit()
        else:
            self.db.rollback()

    def get(self, key):
        res = self.db.execute("SELECT value FROM kvs WHERE key = ?", (key,))
        value = res.fetchone()
        if value:
            return value[0]
        else:
            raise KeyError(key)

    def set(self, key, value):
        try:
            self.db.execute("INSERT INTO kvs VALUES (?, ?)", (key, value))
            self.db.commit()
        except sqlite3.IntegrityError:
            self.db.rollback()
            self.db.execute("UPDATE kvs SET value = ? WHERE key = ?", (value, key))
            self.db.commit()

    def delete(self, key):
        self.db.execute("DELETE FROM kvs WHERE key = ?", (key,))
        self.db.commit()

    def keys(self):
        res = self.db.execute("SELECT key FROM kvs")
        result = res.fetchall()
        result = [x[0] for x in result]  # unpack from per-row
        return result

    def values(self):
        res = self.db.execute("SELECT value FROM kvs")
        result = res.fetchall()
        result = [x[0] for x in result]  # unpack from per-row
        return result
