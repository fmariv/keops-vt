"""Get the size in KB of a given tile or given zoom level"""

import click

from .src.mvt_reader import MVTReader


@click.command(short_help='Get the size of a given tile or zoom level in a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.option('-z', '--zoom')
@click.option('-t', '--tile')
def size(mbtiles, zoom=None, tile=None):
    """Get the size in KB of a given tile or given zoom level.

    $ keops size input.mbtiles --zoom 10

    $ keops size input.mbtiles --tile 10/56/65

    """
    if zoom is None and tile is None:
        click.echo('You have to give at least a tile or a zoom level')
        return
    if zoom is not None and tile is not None:
        click.echo('You only have to give a tile or a zoom level, not both of them')
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
