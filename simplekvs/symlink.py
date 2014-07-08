import os
from errno import *
from .store import Store


def _encode(value):
    if hasattr(value, "encode"):
        value = value.encode("utf8")
    return value


def _decode(value):
    if hasattr(value, "decode"):
        value = value.decode()
    return value


class SymlinkStore(Store):
    """
    A key-value store using symlinks. The filename is the key and the target is
    the value. Restrictions on both vary by filesystem. Because I could.

    .. note::
        For both key and value a UTF-8 string is expected, but a bytes object
        will be converted to UTF-8 if provided. Translation is strict and
        string errors will be raised if it fails.
    
    .. function:: __init__(self, path)
    
        Initialize a symlink store with a directory name. Creates one at the
        destination if it doesn't exist.

        :arg str path: The path to the directory to keep the symlinks in.
    """

    def __init__(self, path):
        self._cache_age = 0
        self._key_cache = []
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path, mode=0o700, exist_ok=True)

    def get(self, key):
        key = _decode(key)
        try:
            value = os.readlink(os.path.join(self.path, key))
            return value
        except OSError as e:
            if e.errno != ENOENT:
                raise e
            raise KeyError(key)

    def set(self, key, value):
        key = _decode(key)
        value = _decode(value)

        try:
            os.symlink(value, os.path.join(self.path, key))

        except OSError as e:
            if e.errno == EEXIST:
                raise KeyError(key)
            else:
                raise

        return key

    def delete(self, key):
        key = _decode(key)
        try:
            os.remove(os.path.join(self.path, key))
        except OSError as e:
            if e.errno == ENOENT:
                raise KeyError(key)
            else:
                raise

    def keys(self):
        mtime = os.path.getmtime(self.path)
        if mtime > self._cache_age:
            self._key_cache = os.listdir(self.path)
            self._cache_age = mtime
        return self._key_cache
