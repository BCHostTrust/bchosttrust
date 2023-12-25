# bchosttrust/bchosttrust/cli/get_rate.py
"""Get the rating of a domain name"""

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

from ..storage import BCHTStorageBase
from ..analysis import get_last_block_hash, search


@click.command("get-rate")
@click.option("--safe/--no-safe", default=True,
              help="Whether to skip the current blocks (i.e. no blocks behind it)")
@click.argument('hostname', type=str)
@click.pass_context
def cli(ctx: click.Context, safe: bool, hostname: str):
    """Get the rating of a domain"""

    storage: BCHTStorageBase = ctx.obj["storage"]

    last_block_hash = None
    try:
        last_block_hash = get_last_block_hash(storage, safe=safe)
    except RuntimeError as e:
        echo(f"Error getting last block hash: {e}", err=True)
        ctx.exit(1)

    rating = search.get_specific_website_rating(
        storage, hostname, last_block_hash)
    echo(rating)
