from .store import Store

import os
from errno import *
class SymlinkStore(Store):
    """
    A key-value store using symlinks. The filename is the key and the target is
    the value. Restrictions on both vary by filesystem.
    
    Mostly a joke/challenge, but who knows what someone could do with it?
    """
    
    ext = ".symdb"
    def __init__(self, storepath):
        if not storepath.endswith(self.ext):
            storepath += self.ext
        self._cache_age = 0
        self._key_cache = []
        self.storepath = storepath
        if not os.path.exists(self.storepath):
            os.makedirs(self.storepath, mode=0o700, exist_ok=True)
            
    def get(self, key):
        try:
            value = os.readlink(os.path.join(self.storepath, key))
            return value
        except OSError as e:
            if e.errno != ENOENT: raise
            return None
    
    def set(self, key, value):
        try:
            os.symlink(value, os.path.join(self.storepath, key))
            
        except OSError as e:
            if e.errno == EEXIST:
                raise KeyError
            else:
                raise
            
        return key
    
    def delete(self, key):
        try:
            os.remove(os.path.join(self.storepath, key))
        except OSError as e:
            if e.errno == ENOENT:
                raise KeyError
            else:
                raise
    
    def keys(self):
        mtime = os.path.getmtime(self.storepath)
        if mtime > self._cache_age:
            self._key_cache = os.listdir(self.storepath)
            self._cache_age = mtime
        return self._key_cache
