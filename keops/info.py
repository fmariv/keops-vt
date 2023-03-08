"""Extract and print the metadata info from a MBTiles file"""

import click

from .src.mvt_printer import MVTPrinter
from .src.mvt_reader import MVTReader
from .src.utils import mbtiles_is_valid


@click.command(short_help='Extract and print the metadata info from a MBTiles file')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.option('-j', '--json', is_flag=True, show_default=True, default=False, help="Print the metadata as a JSON.")
def info(mbtiles: str, json: bool):
    """Extract and print the metadata info from a MBTiles file.

    $ keops info input.mbtiles

    $ keops info -j input.mbtiles

    """
    if not mbtiles_is_valid(mbtiles):
        return

    mvt_reader = MVTReader(mbtiles)

    metadata = mvt_reader.get_metadata()
    if not json:
        # Print as a table
        mvt_printer = MVTPrinter()
        fields = ['name', 'value']
        rows = []
        for name, value in metadata:
            row = (name, value)
            rows.append(row)

        mvt_printer.print(fields, rows)
    else:
        # Print as a json
        metadata_dict = {}
        for name, value in metadata:
            metadata_dict[name] = value
        
        click.echo(metadata_dict)
