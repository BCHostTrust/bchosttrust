# bchosttrust/tests/analysis_tree.py
# test bchosttrust.analysis.tree

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
from bchosttrust.analysis import tree


class BCHTTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.db = BCHTDummyStorage()

        # Not caring about satisfying PoW here
        self.block1 = BCHTBlock(1, b"\x00" * 32, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        self.block2 = BCHTBlock(1, self.block1.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))
        self.block3 = BCHTBlock(1, self.block2.hash, 0, 4, (
            BCHTEntry("www.example.com", attitudes.UPVOTE),
            BCHTEntry("www.example.net", attitudes.UPVOTE)
        ))

        self.db.put(self.block1)
        self.db.put(self.block2)
        self.db.put(self.block3)

    def testTreeRelationship(self):
        list_nodes = tuple(self.db.iter_blocks())
        tree_root = tree.generate_tree(list_nodes, self.block1.hash)

        self.assertEqual(tree_root.children[0].name, self.block2.hash)
        self.assertEqual(
            tree_root.children[0].children[0].name, self.block3.hash)
