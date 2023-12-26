# bchosttrust/tests/consensus_powc.py
# Test bchosttrust.consensus.powc

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
from bchosttrust.consensus import powc
from bchosttrust import BCHTEntry


class BCHTConsensusTestCase(unittest.TestCase):
    def test_pow(self):
        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)

        version = 0
        prev_hash = b"\x00" * 32
        creation_time = 1000

        success_block, _ = powc.attempt(
            version, prev_hash, creation_time, entry_tuple)

        if success_block is not None:
            self.assertLessEqual(int.from_bytes(
                success_block.hash), powc.HASH_TARGET)
        else:
            self.skipTest("Failed to find a hash")


if __name__ == '__main__':
    unittest.main()
