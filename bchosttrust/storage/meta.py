# bchosttrust/bchosttrust/storage/meta.py
# Abstract Base Class (ABC) for storage backends

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
        KeyError
            If the block with the given hash is not found.
        ValueError
            If block_hash is not a valid SHA3-256 hexadecimal hash.
        """

    @abstractmethod
    def put(self, block_data: BCHTBlock):
        """Put the given block into the database.

        Parameters
        ----------
        block_data : BCHTBlock
            The BCHTBlock object to be stored.
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
        KeyError
            If the block with the given hash is not found.
        ValueError
            If block_hash is not a valid SHA3-256 hexadecimal hash.
        """

    @abstractmethod
    def iter_blocks(self) -> typing.Generator[BCHTBlock, None, None]:
        """Return a iterable returning of BCHT Blocks, unordered.

        Yields
        ------
        BCHTBlock
            BCHT Blocks
        """

    @abstractmethod
    def iter_blocks_with_key(self) -> typing.Generator[tuple[bytes, BCHTBlock], None, None]:
        """Return a iterable returning of BCHT Blocks, unordered, with keys.

        Yields
        ------
        tuple[bytes, BCHTBlock]
            hash as keys, BCHT Blocks as values.
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
        KeyError
            If that attibute does not exist.
        ValueError
            If the key is not bytes, or if not accepted by the backend.
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
        KeyError
            If that attibute does not exist.
        ValueError
            If the key is not bytes, or if not accepted by the backend.
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
