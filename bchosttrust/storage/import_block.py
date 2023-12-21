# bchosttrust/bchosttrust/storage/import_block.py
"""Handle import of blocks"""

from ..internal.block import BCHTBlock
from ..consensus import validate
from . import BCHTStorageBase


# Add block into database: backend.put(block)
# Get block from database: backend.get(hash)
# Set attribute: backend.setattr(key, value)
# Get attrioute: backend.getattr(key)

def parse_curr_hashes(backend: BCHTStorageBase) -> tuple[bytes]:
    """Parse the list of hashes of current blocks 
    stored in the database into tuple.

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.

    Returns
    -------
    tuple[bytes]
        List of SHA3-256 hashes, or an 
        empty tuple if "curr_hashes" is not found 
        in the attributes database.
    """

    # 1. Get `curr_hashes` from attribute database (.getattr)
    #    if KeyError (i.e. the key does not exist), just return a empty tuple
    # 2. Slice the retrieved byte by the length of SHA3-256 hashes
    #    Example: https://stackoverflow.com/a/20024864
    # 3. Return the sliced bytes in tuple

    try:
        curr_hashes = backend.getattr(b"curr_hashes")
    except KeyError:
        return tuple()
    return tuple(curr_hashes[i:i+32] for i in range(0, len(curr_hashes), 32))


def add_hash_to_current(backend: BCHTStorageBase, new_hash: bytes):
    """Appends a new hash into the list of current blocks

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    new_hash : bytes
        The hash of the new block to be added.
    """

    # 1. Get `curr_hashes` from attribute database (.getattr)
    #    if KeyError, it should return an empty byte string (b"")
    # 2. Append new_hash into `curr_hashes`
    # 3. Set the new curr_hashes into the attribute database

    try:
        curr_hashes = backend.getattr(b"curr_hashes")
    except KeyError:
        curr_hashes = b""
    curr_hashes += new_hash
    backend.setattr(b"curr_hashes", curr_hashes)


def get_curr_blocks(backend: BCHTStorageBase) -> tuple[BCHTBlock]:
    """Get a list of current blocks

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used

    Returns
    -------
    tuple[BCHTBlock]
        Tuple of BCHTBlock objects
    """

    # 1. Use parse_curr_hashes to get a tuple of hashes
    # 2. For each of them, retrieve them from the blocks database
    #    (backend.get())
    # 3. Put them into a tuple and then return it
    # (2 and 3 can be done in a single line using inline generators)

    hashes = parse_curr_hashes(backend)
    return tuple(backend.get(h) for h in hashes)


def import_block(backend: BCHTStorageBase, block: BCHTBlock):
    """Import a block into the BCHT Database

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    block : BCHTBlock
        The block to be imported.

    Raises
    ------
    ValueError
        If the block is invalid
    """

    # 1. Get the previous block from block.prev_hash.
    # 2. Check the creation time of the previous block.
    #    If this block is earlier than the later block, of course
    #    reject it by raising a ValueError.
    # 2. Check the block against the consensus using the
    #    bchosttrust.consensus.validate function.
    #    If the block fails, reject it by raising a ValueError.
    # 3. Add the hash into the database (backend.put).
    # 4. Check if the `prev_hash` of the block is the same as
    #    `prev_hash` in the attribute database.
    #    - If yes, Append this block's
    #      hash to `curr_hashes` of the attribute database.
    # 5. Otherwise, check if the `prev_hash` of the block is one of the
    #    hashes listed in `curr_hashes`.
    #    - If yes, replace `prev_hash`
    #      in the attribute database with this block's `prev_hash`, and replace
    #      `curr_hashes` in the attribute database with this block's hash.

    prev_block = backend.get(block.prev_hash)
    if prev_block.creation_time > block.creation_time:
        raise ValueError("Block is earlier than the previous block")
    if not validate(block):
        raise ValueError("Block validation failed")
    backend.put(block)
    prev_hash = backend.getattr(b"prev_hash")
    if block.prev_hash == prev_hash:
        add_hash_to_current(backend, block.hash)
    elif block.prev_hash in parse_curr_hashes(backend):
        backend.setattr(b"prev_hash", block.prev_hash)
        backend.setattr(b"curr_hashes", block.hash)
