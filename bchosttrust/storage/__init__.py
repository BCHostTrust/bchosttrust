# bchosttrust/bchosttrust/internal/storage.py
"""Expose common classes and functions directly to the bchosttrust.storage namespace"""

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

import os
import lazy_loader as lazy

from .meta import BCHTStorageBase
from .leveldb import BCHTLevelDBStorage
from .dummy import BCHTDummyStorage
from ..utils import get_data_path

__all__ = ("leveldb", "meta", "dummy")

__getattr__, __dir__, _ = lazy.attach(__name__, __all__)


def get_default_storage() -> BCHTStorageBase:
    r"""The default storage backend.
    It is hoped that one day we can read user's configuration file
    and allow users to choose. But anyway, just make it work for now.

    The default storage backend is a Level DB located at:
    Windows: %LOCALAPPDATA%\BCHostTrust\default.db
    MacOS/Linux/Others: ~/.bchosttrust/default.db

    Returns
    -------
    BCHTStorageBase
        The storage backend.
    """

    db_path = os.path.join(get_data_path(), "default.db")
    return BCHTLevelDBStorage.init_db(
        name=db_path,  # name of the database (directory name)
        create_if_missing=True,  # whether a new database should be created if needed
    )
