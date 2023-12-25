# bchosttrust/tests/analysis_search.py
# test bchosttrust.analysis.search

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

# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

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
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        self.block2 = BCHTBlock(1, self.block1.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
        ))
        self.block3 = BCHTBlock(1, self.block2.hash, 0, 4, (
            BCHTEntry("www.example.org", attitudes.UPVOTE),
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
                attitudes.UPVOTE: 2
            },
            "www.example.net": {
                attitudes.UPVOTE: 1
            },
            "www.example.org": {
                attitudes.UPVOTE: 1
            },
        })

    def testRating(self):
        ratings = search.get_website_rating(self.db, self.block3.hash)

        self.assertDictEqual(ratings, {
            "www.example.com": 2,
            "www.example.net": 1,
            "www.example.org": 1
        })

    def testSpecificRating(self):
        specific_rating = search.get_specific_website_rating(
            self.db, self.block3.hash, "www.example.com")

        self.assertEqual(specific_rating, 2)


if __name__ == '__main__':
    unittest.main()
