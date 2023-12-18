# bchosttrust/bchosttrust/storage/leveldb.py
# Stores everything in LevelDB

from .meta import BCHTStorageBase
from .. import BCHTBlock
from plyvel import DB as LDB
import typing
from type_enforced import Enforcer as enforced


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

    @classmethod
    def init_db(cls, *args, **kwargs) -> typing.Self:
        """Create a BCHT LevelDB Storage backend with parameters passed into a plyvel.DB constructor.
        See https://plyvel.readthedocs.io/en/latest/api.html#DB.__init__ for what to pass into this function.

        Returns
        -------
        BCHTLevelDBStorage
            The storage backend object.
        """
        return cls(LDB(*args, **kwargs))

    @enforced
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
        self.db.put(block_hash, block_data)

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
        RuntimeError
            If the database was closed.
        """

        if len(block_hash) != 32:
            raise ValueError(
                "{} is not a valid SHA3-512 hexadecimal hash.".format(block_hash))
        get_result = self.db.get(block_hash)
        if get_result == None:  # i.e. not found
            raise KeyError("{} not found in the database.".format(block_hash))
        return BCHTBlock.from_raw(get_result)

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
        RuntimeError
            If the database was closed.
        """

        if len(block_hash) != 32:
            raise ValueError(
                "{} is not a valid SHA3-256 hexadecimal hash.".format(block_hash))
        self.db.delete(block_hash)

    @staticmethod
    def _attr_name(attr_name: bytes) -> bytes:
        actual_name = b"attr" + attr_name
        if len(actual_name) == 32:  # Avoid conflicts
            actual_name = b"x" + actual_name
        return actual_name

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
        RuntimeError
            If the database was closed.
        """

        actual_name = self._attr_name(attr_name)
        rtn = self.db.get(actual_name)
        if rtn == None:
            raise KeyError("{} not found in the database.".format(actual_name))
        return rtn

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
        RuntimeError
            If the database was closed.
        """

        actual_name = self._attr_name(attr_name)
        self.db.put(actual_name, content)

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
        RuntimeError
            If the database was closed.
        """

        actual_name = self._attr_name(attr_name)
        self.db.delete(actual_name)

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
