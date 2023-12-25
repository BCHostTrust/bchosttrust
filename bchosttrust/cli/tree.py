# bchosttrust/bchosttrust/cli/tree.py
"""Generate a tree view of blocks"""

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

from anytree import RenderTree
import anytree.render

from ..storage.import_block import get_curr_blocks
from ..storage.meta import BCHTStorageBase
from ..analysis.search import iter_from_block
from ..analysis.tree import generate_tree


@click.command("tree")
@click.option('-s', '--style',
              type=click.Choice(
                  ["ascii", "cont", "round", "double"], case_sensitive=False),
              help="The display style to be used.", default="cont")
@click.pass_context
def cli(ctx: click.Context, style: str):
    """Display the tree of blocks."""

    storage: BCHTStorageBase = ctx.obj["storage"]

    match style:
        case "ascii":
            style = anytree.render.AsciiStyle
        case "cont":
            style = anytree.render.ContStyle
        case "round":
            style = anytree.render.ContRoundStyle
        case "double":
            style = anytree.render.DoubleStyle

    curr_blocks = get_curr_blocks(storage)
    if len(curr_blocks) == 0:
        echo("Create some blocks first.", err=True)
        ctx.exit(1)

    _iter = iter_from_block(storage, curr_blocks[0].hash)
    try:
        while True:
            gen_block = next(_iter)
    except StopIteration:
        pass

    tree = generate_tree(tuple(storage.iter_blocks()), gen_block.hash)

    for pre, _, node in RenderTree(tree, style=style):
        print(f"{pre}{node.name.hex()}")
