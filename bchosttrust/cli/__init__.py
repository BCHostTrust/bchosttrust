# bchosttrust/bchosttrust/cli/__init__.py
"""List all commands in __all__ tuple.
For more information, see bchosttrust/bchosttrust/__main__.py."""


__all__ = (
    "get",
    "import_block",  # Command: import
    "create",
    "get_rate",
    "similar_domain"
)

from importlib import import_module

for mod in __all__:
    mod = import_module(f".{mod}", package=__name__)
