# bchosttrust/bchosttrust/storage/leveldb.py
"""Stores everything in LevelDB"""

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
from plyvel import DB as LDB
from typeguard import typechecked

from .meta import BCHTStorageBase
from .. import exceptions
from .. import BCHTBlock


@typechecked
class BCHTLevelDBStorage(BCHTStorageBase):
    """BCHT LevelDB Storage backend


    Attibutes
    ---------
    db : plyvel.DB
        The LevelDB object this backend is working on. This can be passed into __init__, 
        or created with the init_db classmethod.
        See https://plyvel.readthedocs.io/en/latest/api.html#DB for more usages.
    """

    def __init__(self, db: LDB):
        self.db = db
        self.db_block = db.prefixed_db(b'block-')
        self.db_attr = db.prefixed_db(b'attr-')

    def __str__(self):
        return f"<BCHTLevelDBStorage, db={self.db.__str__()}>"

    @classmethod
    def init_db(cls, *args, **kwargs) -> typing.Self:
        """Create a BCHT LevelDB Storage backend with parameters 
        passed into a plyvel.DB constructor.
        See https://plyvel.readthedocs.io/en/latest/api.html#DB.__init__ 
        for what to pass into this function.

        Returns
        -------
        BCHTLevelDBStorage
            The storage backend object.
        """
        return cls(LDB(*args, **kwargs))

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

        block_hash = block_data.hash
        raw_block_data = block_data.raw
        try:
            self.db_block.put(block_hash, raw_block_data)
        except RuntimeError as e:
            raise exceptions.BCHTDatabaseClosedError(
                "LevelDB backend closed.") from e

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

        if len(block_hash) != 32:
            raise exceptions.BCHTInvalidHashError(
                f"{block_hash} is not a valid SHA3-512 hexadecimal hash.")
        try:
            get_result = self.db_block.get(block_hash)
        except RuntimeError as e:
            raise exceptions.BCHTDatabaseClosedError(
                "LevelDB backend closed.") from e
        if get_result is None:  # i.e. not found
            raise exceptions.BCHTBlockNotFoundError(
                f"{block_hash} not found in the database.")
        return BCHTBlock.from_raw(get_result)

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

        if len(block_hash) != 32:
            raise exceptions.BCHTInvalidHashError(
                f"{block_hash} is not a valid SHA3-256 hexadecimal hash.")
        try:
            self.db_block.delete(block_hash)
        except RuntimeError as e:
            raise exceptions.BCHTDatabaseClosedError(
                "LevelDB backend closed.") from e

    def iter_blocks(self) -> typing.Generator[BCHTBlock, None, None]:
        """Return a iterable returning of BCHT Blocks, unordered.

        Yields
        ------
        BCHTBlock
            BCHT Blocks

        Raises
        ------
        BCHTDatabaseClosedError
            If the database was closed
        """

        try:
            for raw in self.db_block.iterator(include_key=False):
                yield BCHTBlock.from_raw(raw)
        except RuntimeError as e:
            raise exceptions.BCHTDatabaseClosedError(
                "LevelDB backend closed.") from e

    def iter_blocks_with_key(self) -> typing.Generator[tuple[bytes, BCHTBlock], None, None]:
        """Return a iterable returning of BCHT Blocks, unordered, with keys.

        Yields
        ------
        tuple[bytes, BCHTBlock]
            hash as keys, BCHT Blocks as values.

        Raises
        ------
        BCHTDatabaseClosedError
            If the database was closed
        """

        try:
            for key, value in self.db_block:
                yield key, BCHTBlock.from_raw(value)
        except RuntimeError as e:
            raise exceptions.BCHTDatabaseClosedError(
                "LevelDB backend closed.") from e

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

        try:
            rtn = self.db_attr.get(attr_name)
        except RuntimeError as e:
            raise exceptions.BCHTDatabaseClosedError(
                "LevelDB backend closed.") from e
        if rtn is None:
            raise exceptions.BCHTAttributeNotFoundError(
                f"{attr_name} not found in the database.")
        return rtn

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

        try:
            self.db_attr.put(attr_name, content)
        except RuntimeError as e:
            raise exceptions.BCHTDatabaseClosedError(
                "LevelDB backend closed.") from e

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

        try:
            self.db_attr.delete(attr_name)
        except RuntimeError as e:
            raise exceptions.BCHTDatabaseClosedError(
                "LevelDB backend closed.") from e

    def close(self):
        """Closes the LevelDB."""
        if not self.closed:  # Avoid RuntimeError if already closed
            self.db.close()

    def __del__(self):
        if not self.closed:  # Avoid RuntimeError if already closed
            self.db.close()

    @property
    def closed(self):
        """Indicates whether the database is closed, i.e. not avaliable.

        Returns
        -------
        bool
            If False, the backend is no longer usable.
        """

        return self.db.closed
