# bchosttrust/tests/BCHTBlock.py
# Test bchosttrust.BCHTBlock
# canonical: bchosttrust.internal.block.BCHTBlock

# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

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


if __name__ == '__main__':
    unittest.main()
