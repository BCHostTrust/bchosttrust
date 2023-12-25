# bchosttrust/bchosttrust/cli/import_block.py
"""Import blocks from a file or standard input"""

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

    try:
        import_block.import_block(storage, block)
    except exceptions.BCHTConsensusFailedError as e:
        echo(
            f"Import failed: The block failed the consensus: {e}", err=True)
        ctx.exit(4)
    echo(block.hexdigest)
    ctx.exit(0)
