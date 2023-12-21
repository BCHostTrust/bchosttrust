# bchosttrust/bchosttrust/cli/get_rate.py
"""Get the rating of a domain name"""

import click
from click import echo

from .. import search


@click.command("get_rate")
@click.argument('domain_name', type=str)
@click.pass_context
def cli(ctx, domain_name):
    """Get the rating of a domain"""

    # Get the rating of the domain name with the search.get_website_rating function.
