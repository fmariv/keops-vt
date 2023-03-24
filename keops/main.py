"""
Main command group for Keops' CLI.

Subcommands developed as a part of the Keops package have their own
modules under ``keops`` (like ``keops/clip.py``)

"""

import click

from .erase import erase
from .size import size
from .info import info
from .shrink import shrink
from .debug import debug


@click.group()
def main_group():
    """Keops command line interface"""
    pass


# In order to add commands to the group, just import
# and add them to the commands list
commands = [erase, size, info, shrink, debug]

for command in commands:
    main_group.add_command(command)
