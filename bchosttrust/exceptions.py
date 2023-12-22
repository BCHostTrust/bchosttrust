# bchosttrust/bchosttrust/exceptions.py
"""Exceptions for bchosttrust"""


class BCHTInvalidHashError(ValueError):
    """Raised when an invalid value is passed for a SHA3-256 hash."""


class BCHTConsensusFailedError(ValueError):
    """Raised when a block fails the consensus check."""


class BCHTOutOfRangeError(ValueError):
    """Raised when the value or length of a parameter is out of range."""


class BCHTInvalidHostNameError(ValueError):
    """Raised when the value of a hostname is invalid."""


# Blocks

class BCHTInvalidEntryError(ValueError):
    """Raised when a entry is invalid."""


class BCHTInvalidBlockError(ValueError):
    """Raised when the block (or entries) format is/are incorrect."""


# Storage Backends

class BCHTDatabaseClosedError(RuntimeError):
    """Raised in an attempt to access a closed storage backend."""


class BCHTBlockNotFoundError(KeyError):
    """Raised when the block of the given hash is not found."""


class BCHTAttributeNotFoundError(KeyError):
    """Raised when the given attribute is not found."""
