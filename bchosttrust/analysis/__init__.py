# bchosttrust/bchosttrust/analysis/__init__.py
"""Handle Analysis"""

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


import lazy_loader as lazy
from typeguard import typechecked
from ..internal import BCHTBlock
from ..storage import BCHTStorageBase
from ..storage.import_block import parse_curr_hashes

__all__ = ("search", "tree", "horizontal")

__getattr__, __dir__, _ = lazy.attach(__name__, __all__)


@typechecked
def get_last_block_hash(backend: BCHTStorageBase, safe: bool = True) -> bytes:
    """Get the hash of the last block.

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    safe : bool, optional
        Whether to skip the current blocks (i.e. no blocks behind it), by default True

    Returns
    -------
    bytes
        The hash of the last block

    Raises
    ------
    RuntimeError
        If one could not be found.
    """

    if safe:
        try:
            rtn = backend.getattr(b"prev_hash")
        except KeyError as e:
            raise RuntimeError("Unable to find last block hash") from e
        # Special value for null block (i.e. block "before" genesis block)
        if rtn == (b"\x00" * 32):
            raise RuntimeError("Unable to find last block hash")
        return rtn

    curr_blocks = parse_curr_hashes(backend)
    if len(curr_blocks) == 0:
        raise RuntimeError("Unable to find last block hash")
    return curr_blocks[0]


def get_last_block(backend: BCHTStorageBase, safe: bool = True) -> BCHTBlock:
    """Get the BCHTBlock object of the last block.

    Parameters
    ----------
    backend : BCHTStorageBase
        The backend to be used
    safe : bool, optional
        Whether to skip the current block (i.e. no blocks behidn it), by default True

    Returns
    -------
    BCHTBlock
        The object of the last block

    Raises
    ------
    RuntimeError
        If one could not be found.
    """

    last_hash = get_last_block_hash(backend, safe)
    try:
        return backend.get(last_hash)
    except KeyError as e:
        raise RuntimeError("Unable to find last block") from e
