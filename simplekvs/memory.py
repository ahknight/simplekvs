from .store import Store

class MemoryStore(Store):
    """
    A key-value store backed by a dict.
    """
    def __init__(self):
        self._dict = {}
    
    def get(self, key):
        return self._dict[key]
    
    def set(self, key, value):
        self._dict[key] = value
    
    def delete(self, key):
        del self._dict[key]
    
    def keys(self):
        return self._dict.keys()
    
    def values(self):
        return self._dict.values()
