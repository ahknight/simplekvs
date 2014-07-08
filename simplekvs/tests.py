import os
import unittest

from .memory import MemoryStore
from .sqlite import SQLiteStore
from .dbm import DBMStore
from .symlink import SymlinkStore


class StoreTests(object):
    def _set_del_loop(self, count):
        k, v = ("foo", "bar")

        for i in range(100):
            i = str(i)
            with self.assertRaises(KeyError):
                self.kvs[k+i]
            self.kvs[k+i] = v+i
            self.assertEqual(self.kvs[k+i], v+i)

        for i in range(100):
            i = str(i)
            self.assertEqual(self.kvs[k+i], v+i)
            del self.kvs[k+i]
            with self.assertRaises(KeyError):
                self.kvs[k+i]

    def _get_set_loop(self, count):
        k, v = ("foo", "bar")

        # Set
        for i in range(0, count):
            i = str(i)
            self.kvs[k+i] = v+i

        # Get
        for i in range(0, count):
            i = str(i)
            self.assertEqual(self.kvs[k+i], v+i)

    def test_small(self):
        self._set_del_loop(1000)
        self._get_set_loop(1000)

    # def test_large(self):
    #     self._set_del_loop(100000)
    #     self._get_set_loop(100000)

    def test_non_string_arguments(self):
        k, v = (b'0xee', b'0x44')
        self.kvs[k] = v
        self.assertEqual(self.kvs[k], v)


class MemoryStoreTests(unittest.TestCase, StoreTests):
    def setUp(self):
        self.kvs = MemoryStore()

    def tearDown(self):
        del self.kvs


class SQLiteStoreTests(unittest.TestCase, StoreTests):
    def setUp(self):
        self.kvs = SQLiteStore(":memory:")

    def tearDown(self):
        del self.kvs


class DBMStoreTests(unittest.TestCase, StoreTests):
    def setUp(self):
        self.kvs = DBMStore("test.db")

    def tearDown(self):
        del self.kvs
        os.system("rm -r test.db")


class SymlinkStoreTests(unittest.TestCase, StoreTests):
    def setUp(self):
        self.kvs = SymlinkStore("test.symdb")

    def tearDown(self):
        del self.kvs
        os.system("rm -r test.symdb")
