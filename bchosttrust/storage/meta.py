# bchosttrust/bchosttrust/storage/meta.py
# Base Classes of storage backends

import typing
if typing.TYPE_CHECKING:
    from internal import BCHTBlock


class BCHTStorageBase:
    def get(block_hash: str) -> BCHTBlock: ...
    def set(block_hash: str, block_data: BCHTBlock): ...
