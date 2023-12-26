# bchosttrust/bchosttrust/internal/block.py
"""BCHostTrust Blockchain Structure"""

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

import struct
import typing
from dataclasses import dataclass
from hashlib import sha3_256

from typeguard import typechecked

from .. import exceptions


# Typed Dictionaries
class BCHTEntryDict(typing.TypedDict):
    """Dictionary form of BCHTEntry"""

    domain_name: str
    attitude: int


class BCHTBlockDict(typing.TypedDict):
    """Dictionary form of BCHTBlock"""

    version: int
    prev_hash: bytes
    creation_time: int
    nonce: int
    entries: tuple[BCHTEntryDict, ...]

# Object Classes


@dataclass(frozen=True)
@typechecked
class BCHTEntry:
    """A BCHT Entry to be embedded into a BCHTBlock.

    Attributes
    ----------
    domain_name : str
        The domain name in string. Must not exceed 4294967295 charactors.
        Non-ASCII domain names are accepted, but they must be encoded 
        using IDNA encoding.
    attitude : int
        The attitude of the entry. Must be in the range of 0 to 255.
        See bchosttrust.attitudes for more details.
    MAX_DOMAIN_LENGTH : int
        Maximum length accepted in the domain_name field.
        This is the largest number a unsigned 32-bit number can handle.
    MAX_ATTITUDE : int
        Maximum value of the attitude field.
        This is the largest number a unsigned 8-bit number can handle.

    Raises
    ------
    BCHTOutOfRangeError
        Raised when the value or length of a parameter is out of range.
    BCHTInvalidHostNameError
        Raised when the value of a hostname is invalid.
    """

    MAX_DOMAIN_LENGTH = 4294967295  # Length within unsigned integer 32 bit
    MAX_ATTITUDE = 255  # unsigned integer 8 bit

    domain_name: str
    attitude: int

    def __post_init__(self):
        if not 0 <= self.attitude <= self.MAX_ATTITUDE:
            raise exceptions.BCHTOutOfRangeError(
                "Attitude must be within the range of 0 to 255.")
        try:
            domain_name_bytes = self.domain_name.encode("ascii")
        except UnicodeEncodeError as e:
            raise exceptions.BCHTInvalidHostNameError(
                "Domain name must only contain ASCII charactor. "
                "If non-ASCII charactors exists, "
                "escape them with IDNA encoding first.") from e
        if len(domain_name_bytes) > self.MAX_DOMAIN_LENGTH:
            raise exceptions.BCHTOutOfRangeError(
                "Length of domain name must not exceed 4294967295.")

    @classmethod
    def from_raw(cls, raw_bytes: bytes) -> typing.Self:
        """Generate a BCHT Entry object from its bytes form.

        Parameters
        ----------
        raw_bytes : bytes
            The BCHT Entry in bytes

        Returns
        -------
        BCHTEntry
            The BCHT Entry in Python object

        Raises
        ------
        BCHTInvalidEntryError
            If the length of the BCHT Entry is invalid
        """

        raw_bytes_len = len(raw_bytes)
        if raw_bytes_len < 5:
            raise exceptions.BCHTInvalidEntryError(
                "Length of BCHT Entry must be at least 5 bytes.")

        attitude = raw_bytes[0]
        domain_name_len = int.from_bytes(raw_bytes[1:5])

        if (5 + domain_name_len) != raw_bytes_len:
            raise exceptions.BCHTInvalidEntryError(
                "Length of BCHT Entry does not match the one in its header")
        domain_name_bytes = raw_bytes[5:(5 + domain_name_len)]
        domain_name = domain_name_bytes.decode("ascii")

        return cls(domain_name, attitude)

    @classmethod
    def iter_raw_chain(
            cls,
            raw_bytes_chain: bytes) -> typing.Generator[typing.Self, None, None]:
        """Iterate through a raw chain of entries

        Parameters
        ----------
        raw_bytes_chain : bytes
            The raw chain of entries

        Yields
        ------
        BCHTEntry
            The entries on object form

        Raises
        ------
        BCHTInvalidEntryError
            If the length of raw bytes chain is invalid
        """

        try:
            len_entries = len(raw_bytes_chain)
            pt = 0

            while pt < len_entries:
                raw_bytes = raw_bytes_chain[pt:pt+5]

                len_domain = int.from_bytes(raw_bytes[1:5])
                domain_name_bytes = raw_bytes_chain[pt+5:pt+5+len_domain]
                raw_bytes += domain_name_bytes

                pt += 5 + len_domain
                yield BCHTEntry.from_raw(raw_bytes)
        except IndexError as e:
            raise exceptions.BCHTInvalidEntryError(
                "Invalid length of raw bytes chain") from e

    @classmethod
    def from_raw_chain(cls, raw_bytes_chain: bytes) -> tuple[typing.Self, ...]:
        """Convert a raw chain of entries into a tuple of objects

        Parameters
        ----------
        raw_bytes_chain : bytes
            The raw chain of entries

        Returns
        -------
        tuple[typing.Self, ...]
            The tuple of BCHTEntry objects

        Raises
        ------
        BCHTInvalidEntryError
            If the length of raw bytes chain is invalid
        """

        return tuple(cls.iter_raw_chain(raw_bytes_chain))

    @property
    def raw(self) -> bytes:
        """Return the BCHT Entry in its bytes form.

        Returns
        -------
        bytes
            The BCHT Entry in bytes.
        """

        attitude_bytes = struct.pack("B", self.attitude)  # unsigned char
        domain_name_bytes = self.domain_name.encode("ascii")
        domain_name_len = len(domain_name_bytes)
        domain_name_len_bytes = struct.pack(
            ">L", domain_name_len)  # unsigned long

        return attitude_bytes + domain_name_len_bytes + domain_name_bytes

    def dict(self) -> BCHTEntryDict:
        """Return the dictionary form of BCHTEntry

        Returns
        -------
        BCHTEntryDict
            The dictionary form
        """

        return self.__dict__

    @classmethod
    def from_dict(cls, data_dict: BCHTEntryDict) -> typing.Self:
        """Convert the dictionary form of BCHTEntry into object

        Parameters
        ----------
        data_dict : BCHTEntryDict
            The dictionary form

        Returns
        -------
        BCHTEntry
            The object form
        """
        return cls(
            domain_name=data_dict["domain_name"],
            attitude=data_dict["attitude"]
        )


@dataclass(frozen=True)
@typechecked
class BCHTBlock:
    """A BCHT Block in the BCHT Blockchain.

    Attributes
    ----------
    version : int
        The version of the block. Must not exceed 65535
    prev_hash : bytes
        The SHA3-256 hash of the previous block, in bytes.
    creation_time : int
        The creation time in Unix epoch. Must not exceed 18446744073709551615
    nonce : int
        Increases on every attempt to the proof-of-work concensus. Must not exceed 4294967295
    entries : tuple[BCHTEntry, ...]
        A tuple of BCHTEntry objects.
    MAX_VERSION : int
        Maximum value accepted for the version field.
        This is the largest number a unsigned 16-bit number can handle.
    MAX_TIME : int
        Maximum value accepted for the creation_time field.
        This is the largest number a unsigned 64-bit number can handle.
    MAX_NONCE : int
        Maximum value accepted for the nonce field.
        This is the largest number a unsigned 32-bit number can handle.

    Raises
    ------
    BCHTOutOfRangeError
        Raised when the value or length of a parameter is out of range.
    TypeError
        When the type of parameters are not correct
    """

    MAX_VERSION = 65535
    MAX_TIME = 18446744073709551615
    MAX_NONCE = 4294967295

    version: int  # u16, 2 bytes
    prev_hash: bytes  # 32 bytes
    creation_time: int  # u64, 8 bytes
    nonce: int  # u32, 4 bytes
    entries: tuple[BCHTEntry, ...]

    def __post_init__(self):
        if self.version > self.MAX_VERSION:
            raise exceptions.BCHTOutOfRangeError(
                "version must not exceed 65535")
        if not isinstance(self.prev_hash, bytes):
            raise TypeError("prev_hash must be bytes")
        if len(self.prev_hash) != 32:
            raise ValueError("prev_hash must be 32 bytes long")
        if self.creation_time > self.MAX_TIME:
            raise exceptions.BCHTOutOfRangeError(
                "creation_time must not exceed 18446744073709551615")
        if self.nonce > self.MAX_NONCE:
            raise exceptions.BCHTOutOfRangeError(
                "nonce must not exceed 4294967295")
        if not isinstance(self.entries, tuple):
            raise TypeError("entries must be a tuple")
        if any(not isinstance(e, BCHTEntry) for e in self.entries):
            raise TypeError("items in entries must be BCHTEntry objects")

    @classmethod
    def from_raw(cls, raw: bytes) -> typing.Self:
        """Turn raw byte into BCHT Block

        Parameters
        ----------
        raw : bytes
            Raw bytes of the BCHT Block

        Returns
        -------
        BCHTBlock
            The BCHT Block in Python object

        Raises
        ------
        BCHTInvalidBlockError
            If the block (or entries) format is/are incorrect.
        """

        if len(raw) < 46:
            raise exceptions.BCHTInvalidBlockError(
                "BCHTBlock raw format must be longer than 46 bytes")
        version = int.from_bytes(raw[0:2])
        prev_hash = raw[2:34]
        creation_time = int.from_bytes(raw[34:42])
        nonce = int.from_bytes(raw[42:46])
        entries = raw[46:]

        entries_list = BCHTEntry.from_raw_chain(entries)

        return cls(version, prev_hash, creation_time, nonce, entries_list)

    @property
    def raw(self) -> bytes:
        """Return the BCHT Block in its bytes form.

        Returns
        -------
        bytes
            The BCHT Block in bytes.
        """

        version_bytes = struct.pack(">H", self.version)  # unsigned short
        creation_time_bytes = struct.pack(
            ">Q", self.creation_time)  # unsigned long long
        nonce_bytes = struct.pack(">L", self.nonce)  # unsigned long
        entries_bytes = tuple(e.raw for e in self.entries)

        return b"".join((version_bytes,
                        self.prev_hash,
                        creation_time_bytes,
                        nonce_bytes,
                        b"".join(entries_bytes)))

    @property
    def hash(self) -> bytes:
        """Return the hash of the BCHT Block.

        Returns
        -------
        bytes
            The hash value of the BCHT Block.
        """

        h = sha3_256()
        h.update(self.raw)
        return h.digest()

    @property
    def hexdigest(self) -> str:
        """Return the hexadecimal digest of the BCHT Block.

        Returns
        -------
        str
            The hexadecimal digest of the BCHT Block.
        """

        h = sha3_256()
        h.update(self.raw)
        return h.hexdigest()

    def dict(self) -> BCHTBlockDict:
        """Return the dictionary form of BCHTBlock.

        Returns
        -------
        BCHTBlockDict
            The dictionary form.
        """

        return {
            "version": self.version,
            "prev_hash": self.prev_hash,
            "creation_time": self.creation_time,
            "nonce": self.nonce,
            "entries": tuple(entry.dict() for entry in self.entries)
        }

    @classmethod
    def from_dict(cls, data_dict: BCHTBlockDict) -> typing.Self:
        """Convert the dictionary form of BCHTBlock into object

        Parameters
        ----------
        data_dict : BCHTBlockDict
            The dictionary form

        Returns
        -------
        BCHTBlock
            The object form
        """

        return cls(
            version=data_dict["version"],
            prev_hash=data_dict["prev_hash"],
            creation_time=data_dict["creation_time"],
            nonce=data_dict["nonce"],
            entries=tuple(BCHTEntry.from_dict(entry)
                          for entry in data_dict["entries"])
        )
