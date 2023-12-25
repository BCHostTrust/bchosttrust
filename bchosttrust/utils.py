# bchosttrust/bchosttrust/utils.py
"""Utilities used internally"""

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

from platform import system
from pathlib import Path
import os

import click


def get_data_path() -> os.PathLike:
    r"""Returns the data path according to the operating system.

    Windows: %LOCALAPPDATA%\BCHostTrust
    MacOS/Linux/Others: ~/.bchosttrust

    Returns
    -------
    os.PathLike
        The actual path.

    Raises
    ------
    RuntimeError
        If the path cannot be constructed.
    """

    match system():
        case "Windows":
            local_app_data = os.environ.get('LOCALAPPDATA')

            if local_app_data:
                data_dir = os.path.join(local_app_data, "BCHostTrust")
            else:
                raise RuntimeError(
                    "%LOCALAPPDATA% not found as an environment variable.")
        case _:
            home_directory = os.path.expanduser("~")

            if home_directory.startswith("~"):  # Resolve failed
                raise RuntimeError("Failed to resolve user's home directory")

            data_dir = os.path.join(home_directory, ".bchosttrust")
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    return data_dir


def get_cache_path() -> os.PathLike:
    r"""Returns the cache path according to the operating system.
    Contents in this path should not be regared as permamant.

    Windows: %LOCALAPPDATA%\BCHostTrust\cache
    MacOS/Linux/Others: ~/.cache/bchosttrust

    Returns
    -------
    os.PathLike
        The actual path.

    Raises
    ------
    RuntimeError
        If the path cannot be constructed.
    """

    match system():
        case "Windows":
            cache_dir = os.path.join(get_data_path(), "BCHostTrust")
        case _:
            home_directory = os.path.expanduser("~")

            if home_directory.startswith("~"):  # Resolve failed
                raise RuntimeError("Failed to resolve user's home directory")

            cache_dir = os.path.join(home_directory, ".cache", "bchosttrust")
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    return cache_dir


class HashParamType(click.ParamType):  # pylint: disable=too-few-public-methods
    """click.ParamType accepting a SHA3-256 hash, optionally prefixed with 0x."""

    name = "sha3-256 hash in in hex form"

    def convert(self, value, param, ctx):  # pylint: disable=unused-argument, missing-function-docstring, inconsistent-return-statements
        if isinstance(value, str):
            if value.upper() == "GEN":  # Special value for genesis block
                return b"\x00" * 32
            if value[0:2].lower() == "0x":
                value = value[2:]
            if len(value) != 64:
                self.fail("value must be a 32-byte hexadecimal string")
            try:
                return bytes.fromhex(value)
            except ValueError:
                self.fail("Failed to convert value to bytes")
        elif isinstance(value, bytes):
            if len(value) != 32:
                self.fail("The length of value must be 32")
            return value
        else:
            self.fail("Unsupported input")
