"""
:mod:`SimpleKVS` --- A simple and extensable key-value store for Python
=======================================================================

.. moduleauthor:: Adam Knight <adam@movq.us>

In writing several scripts and modules I've run into situations where a local
KVS was needed and found myself writing up ten different versions. When I
realized that one kind of store wasn't up to the task it was a small pain to
swap it out after the fact.

The answer, of course, was to create a generic KVS interface and then give it
some backends so that the right one could be used for the right job. As such,
here we are.


Using the :mod:`simplekvs` Module
---------------------------------

The base class :class:`Store` is abstract and the other classes are built from
it, so start with one of them. :class:`MemoryStore` is backed by a `dict`;
other classes require some kind of specification as to where to keep the data.
That's generally a path, however you can use :class:`SQLiteStore` with a path
of ":memory:" to create the database in memory (good for testing or a
transactional cache).

The :class:`Store` class provides traditional Python dictionary syntax for all
backends.

.. code:: python

    >>> from simplekvs import MemoryStore as store
    >>> data = store()
    >>> data['foo'] = 'bar'
    >>> print(data['foo'])
    bar
    >>> del data['foo']
    >>> print(data['foo'])
    Traceback (most recent call last):
        ...
    KeyError: 'foo'

You can easily replace the store type and keep the same syntax.

.. code:: python

    >>> from simplekvs import SQLiteStore as store
    >>> data = store(":memory:")
    >>> data['foo'] = 'bar'
    >>> print(data['foo'])
    bar
    >>> del data['foo']
    >>> print(data['foo'])
    Traceback (most recent call last):
        ...
    KeyError: 'foo'

"""

__all__ = ("Store", "DBMStore", "MemoryStore", "SQLiteStore", "SymlinkStore")

from .store import Store
from .dbm import DBMStore
from .memory import MemoryStore
from .sqlite import SQLiteStore
from .symlink import SymlinkStore

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
