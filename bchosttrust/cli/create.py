# bchosttrust/bchosttrust/cli/create.py
"""Create block from file input"""

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

import click
from click import echo

from ..internal.block import BCHTEntry
from ..storage import BCHTStorageBase, import_block
from ..consensus.powc import attempt
from .. import exceptions
from ..storage.import_block import get_curr_blocks


@click.command("create")
@click.argument("version", nargs=1, type=int)
@click.argument("creation_time", nargs=1, type=int)
@click.argument("entries", nargs=-1, type=str)
@click.pass_context
def cli(  # pylint: disable=too-many-arguments, too-many-locals
        ctx: click.Context,
        version: int,
        creation_time: int,
        entries: tuple):
    """Create a BCHT block from data supplied.
    Output the raw block data to the `output`.

    version: The version of the block.
    prev_hash: The hash of the previous block. For genesis block, use zeros only.
    creation_time: Creation time in Unix epoch.
    entries: Entry in the format of <hostname> <attitude>

    Example:
    $ bcht create 0 "$(date -u '+%s')" "example.com 0" "example.net 0"
    Working on 000054870dde74253d34661700fe18adee3646cce0415832c0bc9391595ee176
    Block found at nonce 120756
    00007a6c5cbf2e3fd493938ef9b69e2350d2fcefaa448390f1d9fae1c1383cc2
    """

    # `input` is a file opened in read mode.
    # `output` is a file opened in byte write mode.
    # To iterate through the file's lines, use input.readlines()
    # Split every line by space, validate the domain name and atitude
    # (whether they are ascii string and integers), then construct BCHTEntry tuple.
    # After that, Pass the parameters into bchosttrust.consensus.powc.attempt
    # to get a proper nonce.
    # Finally, import the block into the database and write it to `output`.

    storage: BCHTStorageBase = ctx.obj["storage"]

    list_entries = []

    for i, lines in enumerate(entries):
        lines = lines.strip()
        if lines == "":
            continue
        if lines[0] == "#":
            continue

        hostname, attitude_str = lines.split(" ", 2)

        try:
            attitude = int(attitude_str)
        except ValueError:
            echo(f"On line {i}: Attitude is not a valid integer", err=True)
            ctx.exit(1)

        try:
            new_entry = BCHTEntry(hostname, attitude)
        except exceptions.BCHTOutOfRangeError as e:
            echo(f"On line {i}: {e}", err=True)
            ctx.exit(2)
        except exceptions.BCHTInvalidHostNameError:
            echo(f"On line {i}: {hostname} is not a valid hostname", err=True)
            ctx.exit(2)

        list_entries.append(new_entry)

    curr_hashes = get_curr_blocks(storage)
    if len(curr_hashes) == 0:
        echo("Current block not found.", err=True)
        ctx.exit(3)
    echo(f"Working on {curr_hashes[0].hexdigest}", err=True)

    try:
        block, nonce = attempt(version, curr_hashes[0].hash,
                               creation_time, tuple(list_entries))
    except exceptions.BCHTOutOfRangeError as e:
        echo(f"Some value is out of range: {e}", err=True)
        ctx.exit(4)

    if block is None:
        echo("No solution for this block.")
        ctx.exit(5)

    try:
        import_block.import_block(storage, block)
    except exceptions.BCHTConsensusFailedError as e:
        echo(
            f"Import failed: The block failed the consensus: {e}", err=True)
        ctx.exit(4)
    echo(f"Block found at nonce {nonce}")
    echo(block.hexdigest)
    ctx.exit(0)
