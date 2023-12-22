# bchosttrust/bchosttrust/__init__.py
# Expose common classes and functions directly to the bchosttrust namespace
"""BCHostTrust Main Library"""

__version__ = "0.0.1"

__all__ = (
    "analysis",
    "cli",
    "consensus",
    "internal",
    "storage",
    "attitudes",
    "utils",
    "exceptions"
)

from importlib import import_module

from .internal import BCHTBlock, BCHTEntry

for mod in __all__:
    mod = import_module(f".{mod}", package=__name__)
