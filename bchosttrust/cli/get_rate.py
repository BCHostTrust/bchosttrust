# bchosttrust/bchosttrust/cli/get_rate.py
"""Get the rating of a domain name"""

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

    # use search.get_specific_website_rating
