# bchosttrust/bchosttrust/cli/similar_domain.py
"""Get similiar domains"""

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

import json
import click
from click import echo

from ..analysis import get_last_block_hash, search, horizontal
from ..storage import BCHTStorageBase


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
@click.option("--safe/--no-safe", default=True,
              help="Whether to skip the current blocks (i.e. no blocks behind it)")
@click.option('-f', '--format', 'output_format',
              type=click.Choice(("json", "user"), case_sensitive=False),
              default="user")
@click.argument('domain_name', type=str)
@click.pass_context
def cli(ctx: click.Context,  # pylint: disable=too-many-arguments
        threshold_similar: int,
        threshold_sus: int,
        threshold_bad: int,
        safe: bool,
        output_format: str,
        domain_name: str):
    """Get similiar domains"""

    storage: BCHTStorageBase = ctx.obj["storage"]
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
