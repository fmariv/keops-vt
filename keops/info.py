"""Get info related with layers and their features in a given MBTiles"""

import click

from .src.mvt_info_getter import MVTInfoGetter
from .src.utils import tile_zoom_are_valid, mbtiles_is_valid


@click.command(short_help='Get info related with layers and their features of a given tile or zoom level in a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.option('-z', '--zoom', type=int)
@click.option('-t', '--tile', type=str)
def info(mbtiles, zoom: int, tile: str):
    """Get info related with layers and their features of a given tile or zoom level in a MBTiles file.

    $ keops info --zoom 10 input.mbtiles

    $ keops info --tile 10/56/65 input.mbtiles

    """
    if not tile_zoom_are_valid(zoom, tile) and not mbtiles_is_valid(mbtiles):
        return

    mvt_info_getter = MVTInfoGetter()
    if tile is not None and zoom is None:
        pass
    elif tile is None and zoom is not None:
        pass
