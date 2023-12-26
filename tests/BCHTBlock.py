# bchosttrust/tests/BCHTBlock.py
# Test bchosttrust.BCHTBlock
# canonical: bchosttrust.internal.block.BCHTBlock

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
# pylint: disable=line-too-long

import unittest

from bchosttrust import BCHTBlock, BCHTEntry


class BCHTBlockTestCase(unittest.TestCase):
    def test_raw(self):
        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)
        block = BCHTBlock(0, b"\x00" * 32, 1, 4, entry_tuple)

        compare_target = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04\x02\x00\x00\x00\x0ewww.google.com\x03\x00\x00\x00\x0fwww.example.net'
        self.assertEqual(block.raw, compare_target)

    def test_from_raw(self):
        raw = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04\x02\x00\x00\x00\x0ewww.google.com\x03\x00\x00\x00\x0fwww.example.net'
        block = BCHTBlock.from_raw(raw)

        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)
        compare_target_block = BCHTBlock(0, b"\x00" * 32, 1, 4, entry_tuple)

        self.assertEqual(block, compare_target_block)

    def testToDict(self):
        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)
        block_obj = BCHTBlock(0, b"\x00" * 32, 1, 4, entry_tuple)
        block_dict = block_obj.dict()

        self.assertDictEqual(block_dict, {
            "version": 0,
            "prev_hash": b"\x00" * 32,
            "creation_time": 1,
            "nonce": 4,
            "entries": (
                {
                    "domain_name": "www.google.com",
                    "attitude": 2
                },
                {
                    "domain_name": "www.example.net",
                    "attitude": 3
                },
            )
        })

    def testFromDict(self):
        block_dict = {
            "version": 0,
            "prev_hash": b"\x00" * 32,
            "creation_time": 1,
            "nonce": 4,
            "entries": (
                {
                    "domain_name": "www.google.com",
                    "attitude": 2
                },
                {
                    "domain_name": "www.example.net",
                    "attitude": 3
                },
            )
        }
        block_obj = BCHTBlock.from_dict(block_dict)

        self.assertEqual(block_obj.version, 0)
        self.assertEqual(block_obj.prev_hash, b"\x00" * 32)
        self.assertEqual(block_obj.creation_time, 1)
        self.assertEqual(block_obj.nonce, 4)

        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)

        self.assertEqual(block_obj.entries, entry_tuple)


if __name__ == '__main__':
    unittest.main()
