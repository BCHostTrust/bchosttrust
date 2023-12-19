# bchosttrust/bchosttrust/cli/get.py
# Implements the retrieval of block from the database.

from time import strftime
import click
from click import echo

from ..utils import HashParamType


@click.command("get")
@click.option('-f', '--format', 'output_format',
              type=click.Choice(("raw", "user"), case_sensitive=False),
              default="user")
@click.argument('block_hash', type=HashParamType())
@click.pass_context
def cli(ctx, output_format, block_hash):
    """Get a block by its SHA3-256 hash."""

    storage = ctx.storage

    try:
        block = storage.get(block_hash)
    except KeyError:
        echo("Failed to obtain block (not found)", err=True)
        return
    except ValueError:  # This should not happen, HashParamType should have handled this
        echo("Failed to obtain block (invalid hash)", err=True)
        return
    except:
        echo("Failed to obtain block (unknown error)", err=True)
        raise

    time_str = strftime("%a, %d %b %Y %H:%M:%S +0000", block.creation_time)

    match output_format:
        case "raw":
            echo(block.raw)
        case "user":
            echo(f"Version: {block.version}")
            echo(f"Previous hash: {block.prev_hash}")
            echo(f"Creation time: {time_str}")
            echo(f"Nonce: {block.nonce}")
            echo(f"{len(block.entries)} entries:")
            for entry in block.entries:
                echo(f" Domain name: {entry.domain_name}")
                echo(f" Attitude: {entry.attitude}")
