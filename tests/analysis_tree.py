# bchosttrust/tests/tree.py
# test bchosttrust.tree

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

    def testTreeRelationship(self):
        list_nodes = tuple(self.db.iter_blocks())
        tree_root = tree.generate_tree(list_nodes, self.block1.hash)

        self.assertEqual(tree_root.children[0].name, self.block2.hash)
        self.assertEqual(
            tree_root.children[0].children[0].name, self.block3.hash)
