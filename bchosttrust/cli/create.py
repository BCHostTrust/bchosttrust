# bchosttrust/bchosttrust/cli/create.py
"""Create block from file input"""

import typing
import sys

import click
from click import echo

from ..internal.block import BCHTBlock, BCHTEntry
from ..storage import BCHTStorageBase, import_block
from ..consensus.powc import attempt
from .. import exceptions
from ..utils import HashParamType


@click.command("create")
@click.argument("version", nargs=1, type=int)
@click.argument("prev_hash", nargs=1, type=HashParamType)
@click.argument("creation_time", nargs=1, type=int)
@click.argument("entries", nargs=-1, type=str)
@click.pass_context
def cli(  # pylint: disable=too-many-arguments
        ctx: click.Context,
        version: int,
        prev_hash: bytes,
        creation_time: int,
        entries: tuple):
    """Create a BCHT block from data supplied.
    Output the raw block data to the `output`.

    version: The version of the block.
    prev_hash: The hash of the previous block. For genesis block, use zeros only.
    creation_time: Creation time in Unix epoch.
    entries: Entry in the format of <hostname> <attitude>
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
        lines = lines.trim()
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

    try:
        block, _ = attempt(version, prev_hash, creation_time, list_entries)
    except exceptions.BCHTOutOfRangeError as e:
        echo(f"Some value is out of range: {e}", err=True)
        ctx.exit(3)

    if block is None:
        echo("No solution for this block.")
        ctx.exit(4)

    block_hash = block.hash

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
