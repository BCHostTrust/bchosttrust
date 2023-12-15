# bchosttrust/bchosttrust/storage/leveldb.py
# Stores everything in LevelDB

from .meta import BCHTStorageBase

import typing
if typing.TYPE_CHECKING:
    from plyvel import DB as LDB


class BCHTLevelDBStorage(BCHTStorageBase):
    ...
