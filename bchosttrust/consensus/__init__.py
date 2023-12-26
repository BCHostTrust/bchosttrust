# bchosttrust/bchosttrust/consensus/__init__.py
"""Codes related to the consensus mechanism"""

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

import lazy_loader as lazy

from bchosttrust.internal.block import BCHTBlock
from .powc import validate_block_hash
from .limitations import validate_block_limitations

__all__ = ("powc", "limitations")

__getattr__, __dir__, _ = lazy.attach(__name__, __all__)


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
