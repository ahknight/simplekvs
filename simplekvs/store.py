"""
.. module:: store
    :platform: all
    :synopsis:
        Abstract superclass for a key-value store. Implement
        get/set/delete/keys and the rest is free.

    .. note::
        The types for key and value are not defined. Different backing stores
        will have different requirements. Generally-speaking, strings and bytes
        should be safe and other objects might have to be pickled.

"""


class Store(object):
    def get(self, key):
        """
        Returns the value associated with `key`.

        :arg key: the key to retrieve
        :returns: the stored value
        :raises KeyError: if the key does not exist
        """
        raise NotImplementedError

    def set(self, key, value):
        """
        Sets the `key` to the given value.

        :arg key: the key to set
        :arg key: the value to set
        """
        raise NotImplementedError

    def delete(self, key):
        """
        Deletes the value associated with `key`.

        :arg key: the key to delete
        :raises KeyError: if the key does not exist
        """
        raise NotImplementedError

    def keys(self):
        """
        Fetch all keys.

        :returns: a list of all keys in the store
        :rtype: list of keys
        """
        return NotImplementedError

    def __delitem__(self, key):
        return self.delete(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        try:
            v = self.get(key)
            if v is not None:
                return True
        except KeyError:
            pass
        return False

    def __iter__(self):
        for key in self.keys():
            yield key

    def __len__(self):
        return len(self.keys())

