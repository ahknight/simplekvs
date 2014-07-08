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

        self.db = sqlite3.connect(storepath)
        self.db.isolation_level = None

        if is_new:
            self.db.execute("CREATE TABLE kvs (key VARCHAR(255) NOT NULL"
                            " PRIMARY KEY, value TEXT)")

    def __enter__(self):
        self.db.execute("BEGIN TRANSACTION")
        return self

    def __exit__(self, *args):
        # FIXME: ROLLBACK on exceptions
        self.db.execute("COMMIT")

    def get(self, key):
            c = self.db.execute("SELECT value FROM kvs WHERE key = ?", (key,))
            value = c.fetchone()
            if value:
                return value[0]
            else:
                raise KeyError(key)

    def set(self, key, value):
            try:
                self.db.execute("INSERT INTO kvs VALUES (?, ?)", (key, value))
            except sqlite3.IntegrityError:
                self.db.execute("UPDATE kvs SET value = ? WHERE"
                                " key = ?", (value, key))

    def delete(self, key):
            self.db.execute("DELETE FROM kvs WHERE key = ?", (key,))

    def keys(self):
            c = self.db.execute("SELECT key FROM kvs")
            result = c.fetchall()
            result = [x[0] for x in result]  # unpack from per-row
            return result

    def values(self):
            c = self.db.execute("SELECT value FROM kvs")
            result = c.fetchall()
            result = [x[0] for x in result]  # unpack from per-row
            return result
