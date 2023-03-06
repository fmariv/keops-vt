"""Get the size in KB of a given tile or given zoom level"""

import click

from .src.mvt_reader import MVTReader
from .src.utils import tile_zoom_are_valid, mbtiles_is_valid


@click.command(short_help='Get the size of a given tile or zoom level in a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.option('-z', '--zoom', type=int)
@click.option('-t', '--tile', type=str)
def size(mbtiles, zoom: int, tile: str):
    """Get the size in KB of a given tile or given zoom level.

    $ keops size --zoom 10 input.mbtiles

    $ keops size --tile 10/56/65 input.mbtiles

    """
    if not tile_zoom_are_valid(zoom, tile) and not mbtiles_is_valid(mbtiles):
        return

    mvt_reader = MVTReader(mbtiles)
    if tile is not None and zoom is None:
        tile_size = mvt_reader.get_tile_size(tile)
        if tile_size:
            click.echo(f'[>] The size of the tile {tile} is {tile_size} KB')
            if tile_size > 500:
                click.echo(f'Remember that the maximum recommended size of a tile is 500 KB!')
    elif tile is None and zoom is not None:
        zoom_size = mvt_reader.get_zoom_size(zoom)
        if zoom_size:
            click.echo(f'[>] The size of the zoom {zoom} is {zoom_size} KB')
