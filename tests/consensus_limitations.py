# bchosttrust/tests/consensus_limitations.py
# Test bchosttrust.consensus.limitations

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

from bchosttrust.consensus import limitations
from bchosttrust import BCHTEntry, BCHTBlock
from bchosttrust import attitudes


class BCHTConsensusTestCase(unittest.TestCase):
    def test_success(self):
        block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))

        self.assertTrue(limitations.validate_block_limitations(block1))

    def test_failed_toomany(self):
        entries = tuple(BCHTEntry(f"www{i}.example.com", attitudes.UPVOTE)
                        for i in range(limitations.MAX_ENTRIES + 1))
        block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, entries)

        self.assertFalse(limitations.validate_block_limitations(block1))

    def test_failed_empty(self):
        block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, tuple())

        self.assertFalse(limitations.validate_block_limitations(block1))

    def test_failed_duplicate(self):
        block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.com", attitudes.UPVOTE)
        ))

        self.assertFalse(limitations.validate_block_limitations(block1))


if __name__ == '__main__':
    unittest.main()
