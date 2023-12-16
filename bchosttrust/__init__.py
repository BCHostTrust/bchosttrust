# bchosttrust/bchosttrust/__init__.py
# Expose common classes and functions directly to the bchosttrust namespace

__version__ = "0.0.1"

__all__ = ("internal", "consensus", "storage")

from .internal import BCHTBlock, BCHTEntry
