# bchosttrust/bchosttrust/__init__.py
# Expose common classes and functions directly to the bchosttrust namespace
"""BCHostTrust Main Library"""

__version__ = "0.0.1"

__all__ = (
    "utils",
    "analysis",
    "cli",
    "consensus",
    "internal",
    "storage",
    "attitudes",
    "exceptions"
)

import lazy_loader as lazy

from .internal import BCHTBlock, BCHTEntry

__getattr__, __dir__, _ = lazy.attach(__name__, __all__)
