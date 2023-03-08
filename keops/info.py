"""Extract and print metadata info from a MBTiles file"""

import click

from .src.mvt_printer import MVTPrinter
from .src.mvt_reader import MVTReader
from .src.utils import mbtiles_is_valid


@click.command(short_help='Extract and print metadata info from a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
def info(mbtiles: str):
    """Extract and print metadata info from a MBTiles file.

    $ keops info input.mbtiles

    """
    if not mbtiles_is_valid(mbtiles):
        return
