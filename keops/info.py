"""Get info related with layers and their features in a given MBTiles"""

import click

from .src.mvt_info_getter import MVTInfoGetter


@click.command(short_help='Get info related with layers and their features of a given tile or zoom level in a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.option('-z', '--zoom')
@click.option('-t', '--tile')
def info(mbtiles, zoom: int, tile: str):
    """Get info related with layers and their features of a given tile or zoom level in a MBTiles file.

    $ keops info --zoom 10 input.mbtiles

    $ keops info --tile 10/56/65 input.mbtiles

    """
    pass
