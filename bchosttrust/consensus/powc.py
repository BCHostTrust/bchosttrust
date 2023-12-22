# bchosttrust/bchosttrust/consensus/powc.py
"""Handle proof-of-work concensus"""

import typing

from typeguard import typechecked

from ..internal import BCHTBlock, BCHTEntry
from .. import exceptions


# Defines how many zero bytes are required.
# This increases the difficulty of proof-of-work
ZERO_BYTES = 2
HASH_TARGET = int.from_bytes(
    (b"\x00" * ZERO_BYTES) + (b"\xFF" * (32 - ZERO_BYTES)))


@typechecked
def validate_hash(bhash: bytes) -> bool:
    """Validates the given hash (in bytes) according to the proof-of-work target

    Parameters
    ----------
    bhash : bytes
        The hash in bytes to be checked

    Returns
    -------
    bool
        True if the hash fits the requirements
    """

    if bhash == (b"\x00" * 32):
        # Avoid recursion because the prev_hash of the first block is 0
        return False
    return int.from_bytes(bhash) <= HASH_TARGET


@typechecked
def validate_block_hash(block: BCHTBlock) -> bool:
    """Validates the given BCHTBlock according to the proof-of-work target

    Parameters
    ----------
    block : BCHTBlock
        The block to be checked

    Returns
    -------
    bool
        True if the block fits the requirements
    """

    return validate_hash(block.hash)


@typechecked
def attempt(  # pylint: disable=too-many-arguments
        version: int,
        prev_hash: bytes,
        creation_time: int,
        entries: tuple[BCHTEntry, ...],
        maximum_tries: int = BCHTBlock.MAX_NONCE,
        powf: typing.Callable = validate_hash) -> tuple[typing.Union[BCHTBlock, None], int]:
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
        Proof-of-work function accepting the block hash, by default validate_hash

    Returns
    -------
    typing.Union[BCHTBlock, None]
        The one satisfying the proof-of-work, or None if none found
    int
        Number of tries before finding one, or -1 if none found

    Raises
    ------
    BCHTOutOfRangeError
        If any fields exceeds the maximum.
    TypeError
        If any fields are of the wrong type.
    """

    if maximum_tries > BCHTBlock.MAX_NONCE:
        raise exceptions.BCHTOutOfRangeError(
            f"maximum_tries must not exceed {BCHTBlock.MAX_NONCE}")
    for nonce in range(0, maximum_tries):
        block = BCHTBlock(version, prev_hash, creation_time, nonce, entries)
        if powf(block.hash):
            return block, nonce
    return None, -1
