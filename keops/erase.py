"""Drop a tile in a MBTiles file"""

import click

from .src.mvt_eraser import MVTEraser


@click.command(short_help='Erase a tile in a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.argument('z', type=int, required=True)
@click.argument('x', type=int, required=True)
@click.argument('y', type=int, required=True)
def erase(mbtiles, z, x, y):
    # TODO test
    """Erase a tile in a MBTiles file.

    $ keops erase input.mbtiles 10 56 65

    """
    mvt_dropper = MVTEraser(mbtiles)
    mvt_dropper.erase_tile(z, x, y)
