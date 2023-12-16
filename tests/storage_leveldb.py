# bchosttrust/tests/storage_leveldb.py
# Test bchosttrust.storage.BCHTLevelDBStorage
# canonical: bchosttrust.storage.leveldb.BCHTLevelDBStorage

import unittest
import tempfile
from os import path
from bchosttrust import BCHTBlock, BCHTEntry
from bchosttrust.storage import BCHTLevelDBStorage


class BCHTLevelDBStorageTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def testReadWrite(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)
        block = BCHTBlock(0, b"\x00" * 64, 1, 4, entry_tuple)

        backend.put(block)

        self.assertEqual(backend.get(block.hash), block)

    def testDelete(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)
        block = BCHTBlock(0, b"\x00" * 64, 1, 4, entry_tuple)

        backend.put(block)

        backend.delete(block.hash)

        with self.assertRaises(KeyError):
            backend.get(block.hash)

    def testAttrReadWrite(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        attr_key = b"last_block_id"
        attr_value = b"Catgirl-Nya"

        backend.setattr(attr_key, attr_value)

        self.assertEqual(backend.getattr(attr_key), attr_value)

    def testAttrDelete(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        attr_key = b"last_block_id"
        attr_value = b"Catgirl-Nya"

        backend.setattr(attr_key, attr_value)

        backend.delattr(attr_key)

        with self.assertRaises(KeyError):
            backend.getattr(attr_key)

    def testDBClose(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        self.assertFalse(backend.closed)

        backend.close()

        self.assertTrue(backend.closed)

        with self.assertRaises(RuntimeError):
            attr_key = b"last_block_id"
            attr_value = b"Catgirl-Nya"

            backend.setattr(attr_key, attr_value)


if __name__ == '__main__':
    unittest.main()
