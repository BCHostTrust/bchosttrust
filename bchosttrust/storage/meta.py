# bchosttrust/bchosttrust/storage/meta.py
"""Abstract Base Class (ABC) for storage backends"""

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

# pylint: disable=unused-argument

import typing
from abc import abstractmethod, ABCMeta

from ..internal import BCHTBlock


class BCHTStorageBase(metaclass=ABCMeta):
    """Base class of storage backends"""

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def close(self):
        """Close the database."""

    @property
    @abstractmethod
    def closed(self) -> bool:
        """Indicates whether the database is closed, i.e. not avaliable.

        Returns
        -------
        bool
            If False, the backend is no longer usable.
        """
