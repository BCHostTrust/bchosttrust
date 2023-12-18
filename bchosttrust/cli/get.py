# bchosttrust/bchosttrust/cli/get.py
# Implements the retrieval of block from the database.

import click
from click import echo
from time import strftime

from .. import BCHTBlock, BCHTEntry
from ..storage import get_default_storage
from ..utils import HashParamType


@click.command("get")
@click.option('-f', '--format',
              type=click.Choice(("raw", "user"), case_sensitive=False),
              default="user")
@click.argument('hash', type=HashParamType())
def cli(format, hash):
    """Get a block by its SHA3-256 hash."""

    storage = get_default_storage()

    try:
        block = storage.get(hash)
    except KeyError:
        echo("Failed to obtain block (not found)", err=True)
        return None
    except ValueError:  # This should not happen, HashParamType should have handled this
        echo("Failed to obtain block (invalid hash)", err=True)
        return None
    except:
        echo("Failed to obtain block (unknown error)", err=True)
        raise

    time_str = strftime("%a, %d %b %Y %H:%M:%S +0000", block.creation_time)

    match format:
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
