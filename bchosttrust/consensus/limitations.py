# bchosttrust/bchosttrust/consensus/limitations.py
"""Power-unrelated limitations to BCHT blocks"""

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
