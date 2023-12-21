# bchosttrust/bchosttrust/cli/create.py
"""Create block from file input"""

import click
from click import echo

from ..internal.block import BCHTBlock, BCHTEntry
from ..storage import import_block
from ..consensus.powc import attempt


@click.command("create")
@click.argument('input_file', type=click.File('rb'))
@click.argument('output_file', type=click.File('wb'))
@click.pass_context
def cli(ctx, input_file, output_file):
    """Create a BCHT block from data supplied by the file.
    Output the raw block data to the `output`.

    One file may contain serval entries, each occupying one line.
    Every line of the file should be in the format of:
    <domain_name> <attitude>
    """

    # `input` is a file opened in byte read mode.
    # `output` is a file opened in byte write mode.
    # To iterate through the file's lines, use input.readlines()
    # Split every line by space, validate the domain name and atitude
    # (whether they are ascii string and integers), then construct BCHTEntry tuple.
    # After that, Pass the parameters into bchosttrust.consensus.powc.attempt
    # to get a proper nonce.
    # Finally, import the block into the database and write it to `output`.

    storage = ctx.obj["storage"]

    # Remove the following line before start wriiting your code.
    raise NotImplementedError
