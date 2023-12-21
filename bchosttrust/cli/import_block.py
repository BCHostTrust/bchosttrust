# bchosttrust/bchosttrust/cli/import_block.py
"""Import blocks from a file or standard input"""

import click
from click import echo

from ..internal.block import BCHTBlock
from ..storage import import_block


@click.command("import")
@click.argument('input_file', type=click.File('rb'))
@click.pass_context
def cli(ctx, input_file):
    """Imports a BCHT block into the blockchain database."""

    # `input` is a file opened in byte read mode.
    # The entire file can be passed into BCHTBlock.from_raw
    # to generate a block object. After that, it can be passed into
    # bchosttrust.storage.import_block.import_block.

    # Remember to use echo(...) instead of print(...) to return anything
    # to the user. Use echo(..., err=True) to report an error.

    storage = ctx.obj["storage"]

    # Remove the following line before start wriiting your code.
    raise NotImplementedError
