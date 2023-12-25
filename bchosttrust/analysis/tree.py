# bchosttrust/bchosttrust/analysis/tree.py
"""Perform top-to-down searching on the BCHT chain"""

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

from typing import Iterable
from anytree import Node
from typeguard import typechecked

from ..internal import BCHTBlock


@typechecked
def get_child(block_list: Iterable[BCHTBlock], from_block: bytes) -> tuple[BCHTBlock, ...]:
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


@typechecked
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
    Node
        The Node object of the root. The name attibute of it is the hash.
        See https://anytree.readthedocs.io/en/stable/api/anytree.node.html#anytree.node.node.Node
        for more usages.
    """

    root = Node(from_block)
    for child in get_child(block_list, from_block):
        child_block = generate_tree(block_list, child.hash)
        child_block.parent = root
    return root
