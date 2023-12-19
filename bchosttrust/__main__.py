# bchosttrust/bchosttrust/__main__.py
# Handle python3 -m bchosttrust and direct command

import importlib
import click

from .cli import __all__ as list_clis


@click.group()
def cli():
    """BCHostTrust Command-line Script"""


# Registers all commands into the main script.
# To add one into this, follow these steps:
# 1. Create a Python script as bchosttrust/bchosttrust/cli/<command_name>.py
# 2. Write your command, see https://click.palletsprojects.com/en/8.1.x/ for documentations
# 3. Introduce a cli() function as a @click.group() registering all commands into it.
# 4. Add its name into __all__ of bchosttrust/bchosttrust/cli/__init__.py.
for module_name in list_clis:
    # Imports the command-line component from bchosttrust/bchosttrust/cli/<module_name>.py
    # If an error raises here, check __all__ in bchosttrust/bchosttrust/cli/__init__.py
    # to see if any names listed there does not exist.
    module = importlib.import_module(
        f".cli.{module_name}",
        package='bchosttrust'
    )

    # Searches for the cli() click.group or click.command in the module.
    # If an error raises here, check the cli() function in that module file
    # to see if it is prepended with a @click.<...> decorator, or if it exists.
    cli.add_command(module.cli)
