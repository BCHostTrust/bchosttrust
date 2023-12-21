# bchosttrust/bchosttrust/consensus/__init__.py
"""Codes related to the consensus mechanism"""

__all__ = ("powc", "limitations")

from importlib import import_module

from bchosttrust.internal.block import BCHTBlock
from .powc import validate_block_hash
from .limitations import validate_block_limitations

for mod in __all__:
    mod = import_module(f".{mod}", package=__name__)


def validate(block: BCHTBlock) -> bool:
    """Validate a BCHT Block base on all rules.

    Parameters
    ----------
    block : BCHTBlock
        The BCHT Block to be validated

    Returns
    -------
    bool
        Indicates succcess.
    """

    return all((
        validate_block_hash(block),
        validate_block_limitations(block)
    ))
