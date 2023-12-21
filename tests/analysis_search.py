# bchosttrust/tests/analysis_search.py
# test bchosttrust.analysis.search

import unittest

from bchosttrust import BCHTBlock, BCHTEntry
from bchosttrust.storage import BCHTDummyStorage
from bchosttrust import attitudes
from bchosttrust.analysis import search


class BCHTSearchTestCase(unittest.TestCase):
    def setUp(self):
        self.db = BCHTDummyStorage()

        # Not caring about satisfying PoW here
        self.block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.DOWNVOTE)
        ))
        self.block2 = BCHTBlock(1, self.block1.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        self.block3 = BCHTBlock(1, self.block2.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.DOWNVOTE)
        ))

        self.db.put(self.block1)
        self.db.put(self.block2)
        self.db.put(self.block3)

    def testIter(self):
        iterfunc = search.iter_from_block(self.db, self.block3.hash)

        # Note that the blocks appears in reverse order.
        self.assertEqual(iterfunc.__next__(), self.block3)
        self.assertEqual(iterfunc.__next__(), self.block2)
        self.assertEqual(iterfunc.__next__(), self.block1)

        with self.assertRaises(StopIteration):
            iterfunc.__next__()

    def testGetVotes(self):
        votes = search.get_website_votes(self.db, self.block3.hash)

        self.assertDictEqual(votes, {
            "www.example.com": {
                attitudes.UPVOTE: 3
            },
            "www.example.net": {
                attitudes.UPVOTE: 1,
                attitudes.DOWNVOTE: 2
            }
        })

    def testRating(self):
        ratings = search.get_website_rating(self.db, self.block3.hash)

        self.assertDictEqual(ratings, {
            "www.example.com": 3,
            "www.example.net": -1  # (-1) + 1 + (-1)
        })


if __name__ == '__main__':
    unittest.main()
