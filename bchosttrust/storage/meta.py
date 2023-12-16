# bchosttrust/bchosttrust/storage/meta.py
# Base Classes of storage backends

import typing
if typing.TYPE_CHECKING:
    from internal import BCHTBlock


class BCHTStorageBase:
    """Base class of storage backends"""

    def get(block_hash: str) -> BCHTBlock:
        """
        Retrieve a block in the chain by its hash.

        Parameters
        ----------
        block_hash: str
            The hash of the block wanted.

        Returns
        -------
        BCHTBlock
            The block object

        Raises
        ------
        KeyError
            If the block with the given hash is not found.
        ValueError
            If block_hash is not a valid SHA3-512 hash.
        """

        ...

    def set(block_hash: str, block_data: BCHTBlock):
        """
        Put the given block into the database.

        Parameters
        ----------
        block_hash: str
            The hash of the block.
        block_data: BCHTBlock
            The BCHTBlock object to be stored.

        Raises
        ------
        ValueError
            If block_hash is not a valid SHA3-256 hash, or
            block_data is not a valid BCHTBlock.
        """
