# bchosttrust/bchosttrust/consensus/pow.py
# Handle proof-of-work concensus

from ..internal import BCHTBlock, BCHTEntry
import typing

ZERO_BYTES = 3
HASH_TARGET = int.from_bytes(
    (b"\x00" * ZERO_BYTES) + (b"\xFF" * (64 - ZERO_BYTES)))


def validate_hash(hash: bytes):
    return int.from_bytes(hash) <= HASH_TARGET


def validate_block_hash(block: BCHTBlock):
    return validate_hash(block.hash)


def attempt(version: int, prev_hash: bytes, creation_time: int, entries: tuple[BCHTEntry], maximum_tries: int = BCHTBlock.MAX_NONCE, powf: typing.Callable = validate_block_hash) -> (typing.Union[BCHTBlock, None], int):
    """Attempt the proof-of-work by accuminating nonces

    Parameters
    ----------
    version : int
        The version of the block. Must not exceed 65535
    prev_hash : bytes
        The SHA3-512 hash of the previous block, in bytes.
    creation_time : int
        The creation time in Unix epoch. Must not exceed 18446744073709551615
    entries : tuple[BCHTEntry]
        A tuple of BCHTEntry objects.
    maximum_tries : int, optional
        Maximum tries of the proof-of-work, by default and must not exceed BCHTBlock.MAX_NONCE.
    powf : function, optional
        Proof-of-work function accepting the BCHTBlock, by default validate_block_hash

    Returns
    -------
    typing.Union[BCHTBlock, None]
        The one satisfying the proof-of-work, or None if none found
    int
        Number of tries before finding one, or -1 if none found

    Raises
    ------
    ValueError
        If any BCHTBlock values are found to be invalid.
    """

    if nonce > BCHTBlock.MAX_NONCE:
        raise ValueError(
            "nonce must not exceed {}".format(BCHTBlock.MAX_NONCE))
    for nonce in range(0, maximum_tries):
        block = BCHTBlock(version, prev_hash, creation_time, nonce, entries)
        if powf(block):
            return block, nonce
    return None, -1
