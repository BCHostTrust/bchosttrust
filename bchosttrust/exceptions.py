# bchosttrust/bchosttrust/exceptions.py
"""Exceptions for bchosttrust"""

# Copyright (C) 2023  Marco Pui, Cato Yiu, Lewis Chen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# The legal text of GPLv3 and LGPLv3 can be found at
# bchosttrust/gpl-3.0.txt and bchosttrust/lgpl-3.0.txt respectively.


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
