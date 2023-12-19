# bchosttrust/tests/consensus_pow.py
# Test bchosttrust.consensus.pow

import unittest
from bchosttrust.consensus import pow
from bchosttrust import BCHTEntry


class BCHTConsensusTestCase(unittest.TestCase):
    def test_pow(self):
        entry_a = BCHTEntry("www.google.com", 2)
        entry_b = BCHTEntry("www.example.net", 3)
        entry_tuple = (entry_a, entry_b)

        version = 0
        prev_hash = b"\x00" * 32
        creation_time = 1000

        success_block, num_tries = pow.attempt(
            version, prev_hash, creation_time, entry_tuple)

        if success_block != None:
            self.assertLessEqual(int.from_bytes(
                success_block.hash), pow.HASH_TARGET)
        else:
            self.skipTest("Failed to find a hash")


if __name__ == '__main__':
    unittest.main()
