# bchosttrust/bchosttrust/storage/leveldb.py
# Stores everything in LevelDB

import typing
if typing.TYPE_CHECKING:
    from plyvel import DB as LDB
