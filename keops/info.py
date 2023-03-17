"""Extract and print the metadata info from a MBTiles file"""

import click
import json

from .src.mvt_reader import MVTReader
from .src.utils import mbtiles_is_valid


@click.command(short_help='Extract and print the metadata info from a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.option('--show-json', is_flag=True, show_default=True, default=False, help='Show the JSON value [deault: False]')
def info(mbtiles: str, show_json: bool = False):
    """Extract and print the metadata info from a MBTiles file.

    $ keops info input.mbtiles

    $ keops info --show-json input.mbtiles

    """
    if not mbtiles_is_valid(mbtiles):
        return

    mvt_reader = MVTReader(mbtiles)

    metadata = mvt_reader.get_metadata()
    for name, value in metadata:
        if name != 'json':
            click.echo(f'{name}: {value}')
        else:
            if show_json:
                value = json.loads(value)
                click.echo(f'{name}: {json.dumps(value, sort_keys=True, indent=4, ensure_ascii=False)}')
            else:
                try:
                    json.loads(value)
                    click.echo(f'{name}: The value is a valid JSON, use --show-json for dump')
                except ValueError:
                    click.echo(f'{name}: The value is not a valid JSON')
