# bchosttrust/tests/BCHTEntry.py
# Test bchosttrust.BCHTEntry
# canonical: bchosttrust.internal.block.BCHTEntry

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
from bchosttrust import BCHTEntry


class BCHTEntryTestCase(unittest.TestCase):
    def testCreation(self):
        domain_name = "www.example.com"
        attitude = 1

        entry = BCHTEntry(domain_name, attitude)

        self.assertEqual(entry.domain_name, domain_name)
        self.assertEqual(entry.attitude, attitude)

    def testRaw(self):
        entry = BCHTEntry("www.example.net", 2)
        raw = entry.raw

        self.assertEqual(raw, b'\x02\x00\x00\x00\x0fwww.example.net')

    def testFromraw(self):
        raw = b'\x05\x00\x00\x00\x10wwww.example.org'
        entry = BCHTEntry.from_raw(raw)

        self.assertEqual(entry.domain_name, "wwww.example.org")
        self.assertEqual(entry.attitude, 5)

    def testIllegalRawDomainLength(self):
        raw = b'\x05\x00\x00\x00\x10www.example.org'  # actually \x0f in length
        with self.assertRaises(ValueError):
            BCHTEntry.from_raw(raw)

    def testIllegalDomainName(self):
        with self.assertRaises(ValueError):
            BCHTEntry("早上好.中國", 1)

    def testShortRawLength(self):
        raw = b'\x01\x02'
        with self.assertRaises(ValueError):
            BCHTEntry.from_raw(raw)

    def testToDict(self):
        domain_name = "www.example.com"
        attitude = 1
        entry_obj = BCHTEntry(domain_name, attitude)
        entry_dict = entry_obj.dict()

        self.assertEqual(entry_dict["domain_name"], domain_name)
        self.assertEqual(entry_dict["attitude"], attitude)

    def testFromDict(self):
        domain_name = "www.example.com"
        attitude = 1
        entry_dict = {
            "domain_name": domain_name,
            "attitude": attitude
        }
        entry_obj = BCHTEntry.from_dict(entry_dict)

        self.assertEqual(entry_obj.domain_name, domain_name)
        self.assertEqual(entry_obj.attitude, attitude)


if __name__ == '__main__':
    unittest.main()
