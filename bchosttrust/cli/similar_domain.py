# bchosttrust/bchosttrust/cli/similar_domain.py
"""Get similiar domains"""

import json
import click
from click import echo

from ..analysis import get_last_block_hash, search, horizontal


@click.command("similar-domain")
@click.option("--threshold-similar",
              type=float,
              default=horizontal.DEFAULT_MIN_RATIO,
              help="Threshold of similar ratio")
@click.option("--threshold-sus",
              type=int,
              default=horizontal.DEFAULT_SUS,
              help="Threshold of suspicious neibours")
@click.option("--threshold-bad",
              type=int,
              default=horizontal.DEFAULT_BAD,
              help="Threshold of bad neibours")
@click.option("--safe/--no-safe", default=True, help="Whether to skip the current blocks (i.e. no blocks behind it)")
@click.option('-f', '--format', 'output_format',
              type=click.Choice(("json", "user"), case_sensitive=False),
              default="user")
@click.argument('domain_name', type=str)
@click.pass_obj
def cli(obj, threshold_similar, threshold_sus, threshold_bad, safe, output_format, domain_name):
    """Get similiar domains"""

    storage = obj["storage"]
    last_block_hash = get_last_block_hash(storage, safe)

    website_ratings = search.get_website_rating(storage, last_block_hash)
    analysis_result = horizontal.analyse_domain_name(
        domain_name,
        website_ratings,
        threshold_similar,
        threshold_sus,
        threshold_bad
    )

    match output_format:
        case "json":
            echo(json.dumps(analysis_result))
        case "user":
            echo("Better sites:")
            echo("\tAbove SUS threshold:")
            for domain in analysis_result["HIGH"]["SUS"]:
                echo(f"\t\t{domain}")
            echo("\tAbove BAD threshold:")
            for domain in analysis_result["HIGH"]["BAD"]:
                echo(f"\t\t{domain}")
            echo("Worse sites:")
            echo("\tAbove SUS threshold:")
            for domain in analysis_result["LOW"]["SUS"]:
                echo(f"\t\t{domain}")
            echo("\tAbove BAD threshold:")
            for domain in analysis_result["LOW"]["BAD"]:
                echo(f"\t\t{domain}")
