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


@click.group()
@click.pass_context
def main_group():
    """Keops command line interface"""
