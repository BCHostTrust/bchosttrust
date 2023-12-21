# bchosttrust/bchosttrust/storage/leveldb.py
"""Stores everything in LevelDB"""

import typing
from plyvel import DB as LDB

from .meta import BCHTStorageBase
from .. import BCHTBlock


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
        RuntimeError
            If the database was closed.
        """

        block_hash = block_data.hash
        block_data = block_data.raw
        self.db_block.put(block_hash, block_data)

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
        RuntimeError
            If the database was closed.
        """

        if len(block_hash) != 32:
            raise ValueError(
                f"{block_hash} is not a valid SHA3-512 hexadecimal hash.")
        get_result = self.db_block.get(block_hash)
        if get_result is None:  # i.e. not found
            raise KeyError(f"{block_hash} not found in the database.")
        return BCHTBlock.from_raw(get_result)

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
        RuntimeError
            If the database was closed.
        """

        if len(block_hash) != 32:
            raise ValueError(
                f"{block_hash} is not a valid SHA3-256 hexadecimal hash.")
        self.db_block.delete(block_hash)

    def iter_blocks(self) -> typing.Generator[BCHTBlock, None, None]:
        """Return a iterable returning of BCHT Blocks, unordered.

        Yields
        ------
        BCHTBlock
            BCHT Blocks
        """

        for raw in self.db_block.iterator(include_key=False):
            yield BCHTBlock.from_raw(raw)

    def iter_blocks_with_key(self) -> typing.Generator[tuple[bytes, BCHTBlock], None, None]:
        """Return a iterable returning of BCHT Blocks, unordered, with keys.

        Yields
        ------
        tuple[bytes, BCHTBlock]
            hash as keys, BCHT Blocks as values.
        """

        for key, value in self.db_block:
            yield key, BCHTBlock.from_raw(value)

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
        RuntimeError
            If the database was closed.
        """

        rtn = self.db_attr.get(attr_name)
        if rtn is None:
            raise KeyError(f"{attr_name} not found in the database.")
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
        RuntimeError
            If the database was closed.
        """

        self.db_attr.put(attr_name, content)

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
        RuntimeError
            If the database was closed.
        """

        self.db_attr.delete(attr_name)

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
