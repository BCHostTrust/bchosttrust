# bchosttrust/tests/consensus_powc.py
# Test bchosttrust.consensus.powc

# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

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
