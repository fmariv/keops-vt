"""Get the size in KB of a given tile or given zoom level"""

import click

from .src.mvt_reader import MVTReader


@click.command(short_help='Get the size of a given tile or zoom level in a MBTiles file')
@click.option('-z', '--zoom')
@click.option('-t', '--tile')
def size(zoom=None, tile=None):
    # TODO test
    """Get the size in KB of a given tile or given zoom level.

    $ keops size --zoom 10
    $ keops size --tile 10/56/65

    """
    if zoom is None and tile is None:
        click.echo('You have to give at least a tile or a zoom level')
        return
    if zoom is not None and tile is not None:
        click.echo('You only have to give a tile or a zoom level, not both of them')
        return

    # https://stackoverflow.com/questions/60930422/python-click-passing-multiple-key-values-as-options