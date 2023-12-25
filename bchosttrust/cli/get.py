# bchosttrust/bchosttrust/cli/get.py
"""Implements the retrieval of block from the database."""

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

from datetime import datetime
import click
from click import echo

from ..utils import HashParamType
from ..storage import BCHTStorageBase


@click.command("get")
@click.option('-f', '--format', 'output_format',
              type=click.Choice(("raw", "user"), case_sensitive=False),
              default="user")
@click.argument('block_hash', type=HashParamType())
@click.pass_context
def cli(ctx: click.Context, output_format: str, block_hash: bytes):
    """Get a block by its SHA3-256 hash."""

    storage: BCHTStorageBase = ctx.obj["storage"]

    try:
        block = storage.get(block_hash)
    except KeyError:
        echo("Failed to obtain block (not found)", err=True)

        return
    except ValueError:  # This should not happen, HashParamType should have handled this
        echo("Failed to obtain block (invalid hash)", err=True)
        return
    except:
        echo("Failed to obtain block (unknown error)", err=True)
        raise

    time_datetime = datetime.utcfromtimestamp(block.creation_time)
    time_str = time_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')

    match output_format:
        case "raw":
            echo(block.raw)
        case "user":
            echo(f"Version: {block.version}")
            echo(f"Previous hash: {block.prev_hash}")
            echo(f"Creation time: {time_str}")
            echo(f"Nonce: {block.nonce}")
            echo(f"{len(block.entries)} entries:")
            for entry in block.entries:
                echo(f" Domain name: {entry.domain_name}")
                echo(f" Attitude: {entry.attitude}")
