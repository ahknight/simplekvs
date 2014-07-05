from .store import Store

try:
    import dbm.ndbm as dbm #py3
except ImportError:
    import dbm #py2

class DBMStore(Store):
    """
    A key-value store backed by a (N)DBM database.
    """
    ext = ".db"
    def __init__(self, storepath):
        if storepath.endswith(self.ext):
            storepath = storepath[:-len(self.ext)]
            
        self.storepath = storepath
        self.db = dbm.open(storepath, "c", 0o600)
    
    def get(self, key):
        return self.db[key].decode("utf8")
    
    def set(self, key, value):
        self.db[key] = value.encode("utf8")
    
    def delete(self, key):
        del self.db[key]
    
    def keys(self):
        return self.db.keys()
    
    def values(self):
        return self.db.values()

