# bchosttrust/tests/storage_leveldb.py
# Test bchosttrust.storage.BCHTLevelDBStorage
# canonical: bchosttrust.storage.leveldb.BCHTLevelDBStorage

# Copyright (C) 2023  Marco Pui, Cato Yiu, Lewis Chen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# The legal text of GPLv3 and LGPLv3 can be found at
# bchosttrust/gpl-3.0.txt and bchosttrust/lgpl-3.0.txt respectively.

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name

import unittest
import tempfile
from os import path

from bchosttrust import BCHTBlock, BCHTEntry
from bchosttrust.storage import BCHTLevelDBStorage
from bchosttrust import attitudes
from bchosttrust import exceptions


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

        with self.assertRaises(exceptions.BCHTBlockNotFoundError):
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

        with self.assertRaises(exceptions.BCHTAttributeNotFoundError):
            backend.getattr(attr_key)

    def testIteration(self):
        backend = BCHTLevelDBStorage.init_db(
            name=path.join(self.temp_dir.name, "test.db"),
            create_if_missing=True)

        block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        block2 = BCHTBlock(1, block1.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        block3 = BCHTBlock(1, block2.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
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
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        block2 = BCHTBlock(1, block1.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        block3 = BCHTBlock(1, block2.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))

        backend.put(block1)
        backend.put(block2)
        backend.put(block3)

        dict_blocks = dict(backend.iter_blocks_with_key())

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

        with self.assertRaises(exceptions.BCHTDatabaseClosedError):
            attr_key = b"last_block_id"
            attr_value = b"Catgirl-Nya"

            backend.setattr(attr_key, attr_value)

        with self.assertRaises(exceptions.BCHTDatabaseClosedError):
            entry_a = BCHTEntry("www.google.com", 2)
            entry_b = BCHTEntry("www.example.net", 3)
            entry_tuple = (entry_a, entry_b)
            block = BCHTBlock(0, b"\x00" * 32, 1, 4, entry_tuple)

            backend.put(block)


if __name__ == '__main__':
    unittest.main()
