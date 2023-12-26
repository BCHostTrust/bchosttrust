# bchosttrust/tests/import_block.py
# Test bchosttrust.storage.import_block

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

from bchosttrust import BCHTBlock, BCHTEntry
from bchosttrust.storage import BCHTDummyStorage
from bchosttrust.storage import import_block
from bchosttrust import attitudes
from bchosttrust.consensus.powc import attempt


class BCHTImportBlockTestCase(unittest.TestCase):
    def setUp(self):
        self.db = BCHTDummyStorage()

        self.blocks = []
        self.blocks.append(BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        )))
        self.blocks.append(BCHTBlock(1, self.blocks[0].hash, 1, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        )))
        self.blocks.append(BCHTBlock(1, self.blocks[0].hash, 2, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        )))

        for block in self.blocks:
            self.db.put(block)

        # Therefore, the initial chain of blocks is:
        # block[0] -> block[1]
        #        ^ -> block[2]

        # And hence, let's construct curr_hashes and prev_hash manually
        curr_hashes = self.blocks[1].hash + self.blocks[2].hash
        self.db.setattr(b"curr_hashes", curr_hashes)

        self.db.setattr(b"prev_hash", self.blocks[0].hash)

    def tearDown(self):
        self.db.close()

    def test_parse_curr_hashes(self):
        self.assertEqual(import_block.parse_curr_hashes(self.db),
                         (self.blocks[1].hash, self.blocks[2].hash))

    def test_add_hash_to_current(self):
        new_hash = b"".join(i.to_bytes() for i in range(32))

        import_block.add_hash_to_current(self.db, new_hash)

        self.assertEqual(import_block.parse_curr_hashes(self.db),
                         (self.blocks[1].hash, self.blocks[2].hash, new_hash))

    def test_get_curr_blocks(self):
        self.assertEqual(import_block.get_curr_blocks(self.db), (
            self.blocks[1],
            self.blocks[2]
        ))

    def test_import_block_build_on(self):
        # We build a block on top of blocks[1]
        new_block, _ = attempt(1, self.blocks[1].hash, 5, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))

        # By definition of attempt, we are now getting a block
        # with valid nonce.

        # Lets import it
        # The resulting chain would be:
        # blocks[0] -> blocks[1] -> new_block
        #           -> blocks[2]    # This is never to be used

        import_block.import_block(self.db, new_block)

        # Because of our operation,
        # prev_hash should be blocks[1].hash
        # curr_hashes should only contain new_block.hash

        self.assertEqual(self.db.getattr(b"prev_hash"), self.blocks[1].hash)
        self.assertEqual(import_block.parse_curr_hashes(self.db),
                         (new_block.hash, ))

    def test_import_block_fork(self):
        # We build a block on top of blocks[0]
        # Simulating we receiving more tha one blocks simutanously

        new_block, _ = attempt(1, self.blocks[0].hash, 5, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))

        # By definition of attempt, we are now getting a block
        # with valid nonce.

        # Lets import it
        # The resulting chain would be:
        # blocks[0] -> blocks[1]
        #           -> blocks[2]
        #              new_block

        import_block.import_block(self.db, new_block)

        # Because of our operation,
        # prev_hash should still be blocks[10.hash
        # curr_hashes should additionally contain new_block.hash

        self.assertEqual(self.db.getattr(b"prev_hash"), self.blocks[0].hash)
        self.assertEqual(import_block.parse_curr_hashes(self.db), (
            self.blocks[1].hash,
            self.blocks[2].hash,
            new_block.hash
        ))


if __name__ == '__main__':
    unittest.main()
