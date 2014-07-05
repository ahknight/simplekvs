class Store(object):
    '''
    Generic superclass for a key-value store. Implement get/set/delete/keys and the rest is free.
    '''
    def __init__(self, storepath):
        self.storepath = storepath

    def __delitem__(self, key):
        return self.delete(key)
        
    def __setitem__(self, key, value):
        return self.set(key, value)
    
    def __getitem__(self, key):
        return self.get(key)
        
    def __contains__(self, key):
        try:
            v = self.get(key)
            if v != None: return True
        except KeyError:
            pass
        return False
    
    def __iter__(self):
        for key in self.keys():
            yield key
    
    def __len__(self):
        return len(self.keys())
        
    def delete(self, key):
        """Deletes the value associated with `key`."""
        raise NotImplementedError
    
    def set(self, key, value):
        """Sets the `key` to the given value."""
        raise NotImplementedError
    
    def get(self, key):
        """Returns the value associated with `key`."""
        raise NotImplementedError
    
    def keys(self):
        """
        Returns an iterable of all keys in the store.
        """
        return NotImplementedError
