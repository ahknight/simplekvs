from .store import Store

try:
    from cPickle import dumps, loads
except ImportError:
    from pickle import dumps, loads

try:
    import dbm.ndbm as dbm  # py3
except ImportError:
    import dbm  # py2


class DBMStore(Store):
    """
    A key-value store backed by a (N)DBM database.
    """
    def __init__(self, storepath):
        self.storepath = storepath
        self.db = dbm.open(storepath, "c", 0o600)

    def get(self, key):
        k = dumps(key)
        v = loads(self.db[k])
        return v

    def set(self, key, value):
        k = dumps(key)
        v = dumps(value)
        self.db[k] = v

    def delete(self, key):
        k = dumps(key)
        del self.db[k]

    def keys(self):
        return [loads(k) for k in self.db.keys()]

    def values(self):
        return self.db.values()
