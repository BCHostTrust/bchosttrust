# bchosttrust/bchosttrust/storage/dummy.py
# Stores everythin on RAM, vanishes as the program exits
# WARNING: This is not suitable for command-line tests! Use LevelDB in a temporary directory instead.

from .meta import BCHTStorageBase
from .. import BCHTBlock
import typing
from type_enforced import Enforcer as enforced


class BCHTDummyStorage:
    """BCHT in-RAM storage backend"""

    def __init__(self):
        self.db = {}
        self.attr_db = {}
        self.closed = False

    @enforced
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

        if self.closed:
            raise RuntimeError("Database is closed.")
        if len(block_hash) != 32:
            raise ValueError(
                "{} is not a valid SHA3-512 hexadecimal hash.".format(block_hash))
        return self.db[block_hash]  # raise KeyError if not found

    @enforced
    def put(self, block_data: BCHTBlock):
        """Put the given block into the database.

        Parameters
        ----------
        block_data : BCHTBlock
            The BCHTBlock object to be stored.
        """

        if self.closed:
            raise RuntimeError("Database is closed.")
        block_hash = block_data.hash
        self.db[block_hash] = block_data

    @enforced
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

        if self.closed:
            raise RuntimeError("Database is closed.")
        if len(block_hash) != 32:
            raise ValueError(
                "{} is not a valid SHA3-512 hexadecimal hash.".format(block_hash))
        del self.db[block_hash]

    @enforced
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

        if self.closed:
            raise RuntimeError("Database is closed.")
        return self.attr_db[attr_name]  # raise KeyError if not found

    @enforced
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

        if self.closed:
            raise RuntimeError("Database is closed.")
        self.attr_db[attr_name] = content

    @enforced
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

        if self.closed:
            raise RuntimeError("Database is closed.")
        del self.attr_db[attr_name]

    def close(self):
        """Close the database."""

        self.closed = True
        del self.db
        del self.attr_db
