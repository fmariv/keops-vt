"""
Main command group for Keops' CLI.

Subcommands developed as a part of the Keops package have their own
modules under ``keops`` (like ``keops/clip.py``) and are
registered in the 'keops.keops_commands' entry point group in
Keops' ``setup.py``:

    entry_points='''
        [console_scripts]
        keops=keops.main:main_group

        [keops.keops_commands]
        clip=keops.clip:clip
        ...

"""

import click

from .clip import clip


@click.group()
def main_group():
    """Keops command line interface"""
    pass


commands = [clip]

for command in commands:
    main_group.add_command(command)
