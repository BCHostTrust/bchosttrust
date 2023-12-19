# bchosttrust/bchosttrust/search.py
# Perform down-to-top searching on the BCHT chain

from collections import defaultdict

from .storage import BCHTStorageBase
from typing import Generator
from .internal import BCHTBlock
from . import attitudes


def iter_from_block(backend: BCHTStorageBase, bhash: bytes) -> Generator[BCHTBlock, None, None]:
    """Go through every block starting from this block.

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    bhash : bytes
        The hash of the starting block

    Yields
    ------
    BCHTBlock
        The blocks

    Examples
    --------
    >>> from bchosttrust.search import iter_from_block
    >>> from bchosttrust.storage import get_default_storage
    >>> bhash = ... # A hash
    >>> for x in iter_from_block(get_default_storage(), bhash):
    ...     print(x.__repr__())
    BCHTBlock(...)
    BCHTBlock(...)
    # ... Some others until the genesis block
    """

    while True:
        try:
            block = backend.get(bhash)
        except KeyError as e:
            return  # https://peps.python.org/pep-0479/
        bhash = block.prev_hash
        yield block


def get_website_votes(backend: BCHTStorageBase, bhash: bytes) -> defaultdict[str, defaultdict[int, int]]:
    """Count the number of votes with different attitudes on websites

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    bhash : bytes
        The hash of the starting block. See iter_from_block(...) for more details.

    Returns
    -------
    colections.defaultdict[str, dict[int, int]]
        A dictionary with website domain names as key, and a dictionary
        as its value. The later dictionary is indexed by the attitude and 
        contains the number of votes.
        defaultdict is an instance of dict, so it can be treated
        as if it is an ordinary dictionary.
    """

    result = defaultdict(lambda: defaultdict(int))

    for block in iter_from_block(backend, bhash):
        for entry in block.entries:
            result[entry.domain_name][entry.attitude] += 1

    return result


def get_website_rating(
        backend: BCHTStorageBase,
        bhash: bytes) -> dict[str, int]:
    """Get the rating of a hostname by their votes.

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    bhash : bytes
        The hash of the starting block. See iter_from_block(...) for more details.

    Returns
    -------
    dict[str, int]
        A dictionary with website domain names as key, and its rating as the value.
    """

    result = {}
    for name, votes in get_website_votes(backend, bhash).items():
        result[name] = sum((attitudes.WEIGHTS[att] * num)
                           for att, num in votes.items())
    return result
