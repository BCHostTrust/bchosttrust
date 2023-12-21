# bchosttrust/bchosttrust/analysis/tree.py
"""Perform top-to-down searching on the BCHT chain"""

from typing import Iterable
from anytree import Node

from ..internal import BCHTBlock


def get_child(block_list: Iterable[BCHTBlock], from_block: bytes) -> tuple[BCHTBlock]:
    """Get a list of children of a BCHTBlock.

    Parameters
    ----------
    block_list : Iterable[BCHTBlock]
        A list of block, typically returned by tuple(backend.iter_blocks())
    from_block : bytes
        The hash of the starting block

    Returns
    -------
    tuple[BCHTBlock]
        List of children
    """

    return tuple(block for block in block_list if block.prev_hash == from_block)


def generate_tree(block_list: Iterable[BCHTBlock], from_block: bytes) -> Node:
    """Generate a tree of blocks in the BCHT chain.

    Parameters
    ----------
    block_list : Iterable[BCHTBlock]
        A list of block, typically returned by tuple(backend.iter_blocks())
    from_block : bytes
        The hash of the starting block

    Returns
    -------
    anytree.Node
        The Node object of the root. The name attibute of it is the hash.
        See https://anytree.readthedocs.io/en/stable/api/anytree.node.html#anytree.node.node.Node
        for more usages.
    """

    root = Node(from_block)
    for child in get_child(block_list, from_block):
        child_block = generate_tree(block_list, child.hash)
        child_block.parent = root
    return root
