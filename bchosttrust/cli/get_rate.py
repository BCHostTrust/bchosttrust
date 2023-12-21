# bchosttrust/bchosttrust/cli/get_rate.py
"""Get the rating of a domain name"""

import click
from click import echo

from ..analysis import search


@click.command("get-rate")
@click.argument('domain_name', type=str)
@click.pass_obj
def cli(obj, domain_name):
    """Get the rating of a domain"""

    # Get the rating of the domain name with the search.get_website_rating function.

    storage = obj["storage"]

    # Remove the following line before start wriiting your code.
    raise NotImplementedError
