# bchosttrust/tests/consensus_limitations.py
# Test bchosttrust.consensus.limitations

import unittest
from bchosttrust.consensus import limitations
from bchosttrust import BCHTEntry, BCHTBlock
from bchosttrust import attitudes


class BCHTConsensusTestCase(unittest.TestCase):
    def test_success(self):
        block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.DOWNVOTE)
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
            BCHTEntry("www.example.com", attitudes.DOWNVOTE)
        ))

        self.assertFalse(limitations.validate_block_limitations(block1))


if __name__ == '__main__':
    unittest.main()
