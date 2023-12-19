# bchosttrust/bchosttrust/internal/storage.py
# Expose common classes and functions directly to the bchosttrust.storage namespace

__all__ = ("leveldb", "meta", "dummy")

from .meta import BCHTStorageBase
from .leveldb import BCHTLevelDBStorage
from .dummy import BCHTDummyStorage
from ..utils import get_data_path
import os


def get_default_storage() -> BCHTStorageBase:
    """The default storage backend.
    It is hoped that one day we can read user's configuration file
    and allow users to choose. But anyway, just make it work for now.

    The default storage backend is a Level DB located at:
    Windows: %LOCALAPPDATA%\BCHostTrust\default.db
    MacOS/Linux/Others: ~/.bchosttrust/default.db

    Returns
    -------
    BCHTStorageBase
        The storage backend.
    """

    db_path = os.path.join(get_data_path(), "default.db")
    return BCHTLevelDBStorage.init_db(
        name=db_path,  # name of the database (directory name)
        create_if_missing=True,  # whether a new database should be created if needed
    )
