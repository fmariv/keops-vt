"""Extract and print the metadata info from a MBTiles file"""

import click

import pprint

from .src.mvt_reader import MVTReader
from .src.utils import mbtiles_is_valid


@click.command(short_help='Extract and print the metadata info from a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
def info(mbtiles: str):
    """Extract and print the metadata info from a MBTiles file.

    $ keops info input.mbtiles

    $ keops info -j input.mbtiles

    """
    if not mbtiles_is_valid(mbtiles):
        return

    mvt_reader = MVTReader(mbtiles)

    metadata = mvt_reader.get_metadata()
    metadata_dict = {}
    for name, value in metadata:
        metadata_dict[name] = value

    # TODO better print
    pprint.pprint(metadata_dict)
