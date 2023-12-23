# bchosttrust/bchosttrust/cli/import_block.py
"""Import blocks from a file or standard input"""

import typing

import click
from click import echo

from ..internal.block import BCHTBlock
from ..storage import import_block
from .. import exceptions


@click.command("import")
@click.option("--override/--no-override", default=False,
              help="Whether to override existing block of the same hash.")
@click.argument('input_file', type=click.File('rb'))
@click.pass_context
def cli(ctx: click.Context, override: bool, input_file: typing.BinaryIO):
    """Manually import a BCHT block into the blockchain database."""

    # `input` is a file opened in byte read mode.
    # The entire file can be passed into BCHTBlock.from_raw
    # to generate a block object. After that, it can be passed into
    # bchosttrust.storage.import_block.import_block.

    # Remember to use echo(...) instead of print(...) to return anything
    # to the user. Use echo(..., err=True) to report an error.

    storage = ctx.obj["storage"]

    block_data = input_file.read()

    try:
        block = BCHTBlock.from_raw(block_data)
    except exceptions.BCHTInvalidBlockError as e:
        echo(f"Import failed: Invalid block: {e}", err=True)
        ctx.exit(1)

    block_hash = block.hash

    if not override:
        try:
            _ = storage.get(block_hash)
        except exceptions.BCHTBlockNotFoundError:
            pass
        else:
            echo(
                f"Import failed: A block with the hash {block.hexdigest} already exists.", err=True)
            echo("Use --override to force-import this block.")
            ctx.exit(2)

    if block_hash == (b"\x00" * 32):
        # This is the genesis block, validation would always fail.
        # Therefore, we are going to construct the attributes ourself.
        echo("WARNING: Importing genesis block.", err=True)

        storage.put(block)
        storage.delattr(b"prev_hash")
        storage.setattr(b"curr_hashes", block_hash)
    else:
        try:
            import_block.import_block(storage, block)
        except exceptions.BCHTConsensusFailedError as e:
            echo(
                f"Import failed: The block failed the consensus: {e}", err=True)
            ctx.exit(3)
    echo(block.hexdigest)
    ctx.exit(0)
