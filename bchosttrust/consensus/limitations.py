# bchosttrust/bchosttrust/consensus/limitations.py
"""Power-unrelated limitations to BCHT blocks"""

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

from collections import Counter

from typeguard import typechecked

from bchosttrust.internal.block import BCHTBlock


MAX_ENTRIES = 10


@typechecked
def validate_block_limitations(block: BCHTBlock) -> bool:
    """validate a BCHT Block according to power-unrelated consensus

    Parameters
    ----------
    block : BCHTBlock
        The BCHTBlock to be validated

    Returns
    -------
    bool
        Indicating success
    """

    len_block_entries = len(block.entries)

    if len_block_entries == 0:
        return False

    if len_block_entries > 1:
        if len_block_entries > MAX_ENTRIES:
            return False

        counter_domain = Counter(entry.domain_name for entry in block.entries)
        if counter_domain.most_common(1)[0][1] > 1:  # The most common one > 1
            return False

    return True
