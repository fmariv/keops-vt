"""Extract and print the metadata info from a MBTiles file"""

import click

import json

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
    for name, value in metadata:
        if name != 'json':
            click.echo(f'{name}: {value}')
        else:
            value = json.loads(value)
            click.echo(f'{name}: {json.dumps(value, sort_keys=True, indent=4, ensure_ascii=False)}')
