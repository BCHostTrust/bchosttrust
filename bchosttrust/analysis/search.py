# bchosttrust/bchosttrust/analysis/search.py
"""Perform down-to-top searching on the BCHT chain"""

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

from collections import defaultdict
from typing import Generator

from typeguard import typechecked

from ..storage import BCHTStorageBase
from ..internal import BCHTBlock
from .. import attitudes


@typechecked
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
        except KeyError:
            return  # https://peps.python.org/pep-0479/
        bhash = block.prev_hash
        yield block


@typechecked
def get_website_votes(
        backend: BCHTStorageBase,
        bhash: bytes) -> defaultdict[str, defaultdict[int, int]]:
    """Count the number of votes with different attitudes on websites

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    bhash : bytes
        The hash of the starting block. See iter_from_block(...) for more details.

    Returns
    -------
    colections.defaultdict[str, defaultdict[int, int]]
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


@typechecked
def get_specific_website_votes(
        backend: BCHTStorageBase,
        bhash: bytes,
        hostname: str) -> defaultdict[int, int]:
    """Get the number of votes with different attitudes on a specific website

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    bhash : bytes
        The hash of the starting block. See iter_from_block(...) for more details.
    hostname : str
        The hostname to be checked.

    Returns
    -------
    defaultdict[int, int]
        A dictionary with attitudes as keys and votes as values.
    """

    result: defaultdict[int, int] = defaultdict(int)

    for block in iter_from_block(backend, bhash):
        for entry in block.entries:
            if entry.domain_name == hostname:
                result[entry.attitude] += 1

    return result


@typechecked
def get_website_rating(
        backend: BCHTStorageBase,
        bhash: bytes) -> dict[str, int]:
    """Get the rating of hostnames by their votes.

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


@typechecked
def get_specific_website_rating(
        backend: BCHTStorageBase,
        bhash: bytes,
        hostname: str) -> int:
    """Get the rating of hostnames by their votes.

    Parameters
    ----------
    backend : BCHTStorageBase
        The storage backend to be used.
    bhash : bytes
        The hash of the starting block. See iter_from_block(...) for more details.
    hostname : str
        The hostname to be checked.

    Returns
    -------
    int
        The rating of the hostname.
    """

    votes = get_specific_website_votes(backend, bhash, hostname)

    return sum((attitudes.WEIGHTS[att] * num) for att, num in votes.items())
