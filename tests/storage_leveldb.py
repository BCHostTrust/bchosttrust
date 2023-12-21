# bchosttrust/tests/storage_leveldb.py
# Test bchosttrust.storage.BCHTLevelDBStorage
# canonical: bchosttrust.storage.leveldb.BCHTLevelDBStorage

# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest
import tempfile
from os import path

from bchosttrust import BCHTBlock, BCHTEntry
from bchosttrust.storage import BCHTLevelDBStorage
from bchosttrust import attitudes


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
        block = BCHTBlock(0, b"\x00" * 32, 1, 4, entry_tuple)

        backend.put(block)

        self.assertEqual(backend.get(block.hash), block)

    def testDelete(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)
        block = BCHTBlock(0, b"\x00" * 32, 1, 4, entry_tuple)

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

    def testIteration(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.DOWNVOTE)
        ))
        block2 = BCHTBlock(1, block1.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        block3 = BCHTBlock(1, block2.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.DOWNVOTE)
        ))

        backend.put(block1)
        backend.put(block2)
        backend.put(block3)

        list_blocks = tuple(backend.iter_blocks())

        for block in (block1, block2, block3):
            self.assertTrue(block in list_blocks)

    def testIterationDict(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.DOWNVOTE)
        ))
        block2 = BCHTBlock(1, block1.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        block3 = BCHTBlock(1, block2.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.DOWNVOTE)
        ))

        backend.put(block1)
        backend.put(block2)
        backend.put(block3)

        dict_blocks = {key: value for key,
                       value in backend.iter_blocks_with_key()}

        for block in (block1, block2, block3):
            self.assertTrue(block.hash in dict_blocks)
            self.assertEqual(dict_blocks[block.hash], block)

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

        with self.assertRaises(RuntimeError):
            entry_a = BCHTEntry("www.google.com", 2)
            entry_b = BCHTEntry("www.example.net", 3)
            entry_tuple = (entry_a, entry_b)
            block = BCHTBlock(0, b"\x00" * 32, 1, 4, entry_tuple)

            backend.put(block)


if __name__ == '__main__':
    unittest.main()
