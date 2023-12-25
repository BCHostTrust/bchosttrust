# bchosttrust/bchosttrust/storage/dummy.py
"""Stores everythin on RAM, vanishes as the program exits
WARNING: This is not suitable for command-line tests! 
         Use LevelDB in a temporary directory instead."""

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

import typing
from typeguard import typechecked

from .meta import BCHTStorageBase
from .. import exceptions
from .. import BCHTBlock


@typechecked
class BCHTDummyStorage(BCHTStorageBase):
    """BCHT in-RAM storage backend"""

    def __init__(self):
        self.db = {}
        self.attr_db = {}
        self._closed = False

    def __str__(self):
        return "<BCHTDummyStorage>"

    def get(self, block_hash: bytes) -> BCHTBlock:
        """Retrieve a block in the chain by its hash.

        Parameters
        ----------
        block_hash : bytes
            The hexadecimal hash of the block wanted.

        Returns
        -------
        BCHTBlock
            The block object

        Raises
        ------
        BCHTBlockNotFoundError
            If the block with the given hash is not found.
        BCHTInvalidHashError
            If block_hash is not a valid SHA3-256 hexadecimal hash.
        BCHTDatabaseClosedError
            If the database was closed.
        """

        if self.closed:
            raise exceptions.BCHTDatabaseClosedError("Database is closed.")
        if len(block_hash) != 32:
            raise exceptions.BCHTInvalidHashError(
                f"{block_hash} is not a valid SHA3-512 hexadecimal hash.")
        try:
            return self.db[block_hash]  # raise KeyError if not found
        except KeyError as e:
            raise exceptions.BCHTBlockNotFoundError(
                f"Block {block_hash} not found in the database.") from e

    def put(self, block_data: BCHTBlock):
        """Put the given block into the database.

        Parameters
        ----------
        block_data : BCHTBlock
            The BCHTBlock object to be stored.

        Raises
        ------
        BCHTDatabaseClosedError
            If the database was closed.
        """

        if self.closed:
            raise exceptions.BCHTDatabaseClosedError("Database is closed.")
        block_hash = block_data.hash
        self.db[block_hash] = block_data

    def delete(self, block_hash: bytes):
        """Delete a block in the chain by its hash.

        Parameters
        ----------
        block_hash : str
            The hexadecimal hash of the block wanted.

        Raises
        ------
        BCHTInvalidHashError
            If block_hash is not a valid SHA3-256 hexadecimal hash.
        BCHTDatabaseClosedError
            If the database was closed.
        """

        if self.closed:
            raise exceptions.BCHTDatabaseClosedError("Database is closed.")
        if len(block_hash) != 32:
            raise exceptions.BCHTInvalidHashError(
                f"{block_hash} is not a valid SHA3-512 hexadecimal hash.")
        del self.db[block_hash]

    def iter_blocks(self) -> typing.Generator[BCHTBlock, None, None]:
        """Return a iterable returning of BCHT Blocks, unordered.

        Yields
        ------
        BCHTBlock
            BCHT Blocks

        Raises
        ------
        BCHTDatabaseClosedError
            If the database was closed.
        """

        if self.closed:
            raise exceptions.BCHTDatabaseClosedError("Database is closed.")

        for _, value in self.db.items():
            yield value

    def iter_blocks_with_key(self) -> typing.Generator[tuple[bytes, BCHTBlock], None, None]:
        """Return a iterable returning of BCHT Blocks, unordered, with keys.

        Yields
        ------
        tuple[bytes, BCHTBlock]
            hash as keys, BCHT Blocks as values.

        Raises
        ------
        BCHTDatabaseClosedError
            If the database was closed.
        """

        if self.closed:
            raise exceptions.BCHTDatabaseClosedError("Database is closed.")

        for key, value in self.db.items():
            yield key, value

    def getattr(self, attr_name: bytes) -> bytes:
        """Retrieve an attibute from the database

        Parameters
        ----------
        attr_name : bytes
            The name of the attibute

        Returns
        -------
        bytes
            The content of the attibute

        Raises
        ------
        BCHTAttributeNotFoundError
            If that attibute does not exist.
        ValueError
            If the key is not bytes, or if not accepted by the backend.
        BCHTDatabaseClosedError
            If the database was closed.
        """

        if self.closed:
            raise exceptions.BCHTDatabaseClosedError("Database is closed.")
        try:
            return self.attr_db[attr_name]  # raise KeyError if not found
        except KeyError as e:
            raise exceptions.BCHTAttributeNotFoundError(
                f"Attribute {attr_name} not found.") from e

    def setattr(self, attr_name: bytes, content: bytes):
        """Set an attibute into the database

        Parameters
        ----------
        attr_name : bytes
            The name of the attibute
        content : bytes
            Contents to be stored

        Raises
        ------
        ValueError
            If the data or key is not bytes, or if not accepted by the backend.
        BCHTDatabaseClosedError
            If the database was closed.
        """

        if self.closed:
            raise exceptions.BCHTDatabaseClosedError("Database is closed.")
        self.attr_db[attr_name] = content

    def delattr(self, attr_name: bytes):
        """Delete an attibute from the database

        Parameters
        ----------
        attr_name : bytes
            The name of the attibute

        Raises
        ------
        ValueError
            If the key is not bytes, or if not accepted by the backend.
        BCHTDatabaseClosedError
            If the database was closed.
        """

        if self.closed:
            raise exceptions.BCHTDatabaseClosedError("Database is closed.")
        del self.attr_db[attr_name]

    @property
    def closed(self):
        return self._closed

    def close(self):
        """Close the database."""

        self._closed = True
        del self.db
        del self.attr_db
