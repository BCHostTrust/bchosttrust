# bchosttrust/bchosttrust/cli/get_rate.py
"""Get the rating of a domain name"""

import click
from click import echo

from ..analysis import get_last_block_hash, search


@click.command("get-rate")
@click.option("--safe/--no-safe", default=True,
              help="Whether to skip the current blocks (i.e. no blocks behind it)")
@click.argument('domain_name', type=str)
@click.pass_context
def cli(ctx, safe, domain_name):
    """Get the rating of a domain"""

    # Get the rating of the domain name with the search.get_website_rating function.

    storage = ctx.obj["storage"]

    # Remove the following line before start wriiting your code.
    raise NotImplementedError
