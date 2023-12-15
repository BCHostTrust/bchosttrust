# bchosttrust/tests/BCHTEntry.py
# Test nchosttrust.internal.BCHTEntry

import unittest
from bchosttrust.internal import BCHTEntry


class BCHTEntryTestCase(unittest.TestCase):
    def testCreation(self):
        domain_name = "www.example.com"
        attitude = 1

        entry = BCHTEntry(domain_name, attitude)

        self.assertEqual(entry.domain_name, domain_name)
        self.assertEqual(entry.attitude, attitude)

    def testRaw(self):
        entry = BCHTEntry("www.example.net", 2)
        raw = entry.raw()

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

    def testShortRawLength(self):
        raw = b'\x01\x02'
        with self.assertRaises(ValueError):
            BCHTEntry.from_raw(raw)


if __name__ == '__main__':
    unittest.main()
