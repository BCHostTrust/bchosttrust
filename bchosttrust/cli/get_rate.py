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

    # Get the rating of the domain name with the search.get_website_rating function.

    storage: BCHTStorageBase = ctx.obj["storage"]

    try:
        last_block_hash = get_last_block_hash(storage, safe)
    except RuntimeError:
        echo("Cannot find last block hash", err=True)
        ctx.exit(1)

    ratings = search.get_website_rating(storage, last_block_hash)

    if hostname in ratings:
        echo(ratings[hostname])
        ctx.exit(0)

    echo("WARNING: rating not found", err=True)
    echo(0)
    ctx.exit(2)
