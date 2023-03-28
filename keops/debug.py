"""Debug a MBTiles file: get info related with layers and their features in a given MBTiles"""

import click

from .src.mvt_printer import MVTPrinter
from .src.mvt_debugger import MVTDebugger
from .src.utils import mbtiles_is_valid, get_spinner


@click.command(short_help='Debug a MBTiles file: get info related with layers and their features in a given MBTiles')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.option('-z', '--zoom', type=int, help='Zoom of the MBTiles to get the size of')
@click.option('-t', '--tile', type=str, help='Tile of the MBTiles to get the size of')
def debug(mbtiles: str, zoom: int, tile: str):
    """Debug a MBTiles file: get info related with layers and their features in a given MBTiles.

    $ keops debug --zoom 10 input.mbtiles

    $ keops debug --tile 10/56/65 input.mbtiles

    """
    if not mbtiles_is_valid(mbtiles):
        return

    mvt_printer = MVTPrinter()
    mvt_debugger = MVTDebugger(mbtiles)
    decoded, layers_dict = None, None

    spinner = get_spinner('Debugging the MBTiles...')
    spinner.start()
    if tile is None and zoom is None:
        # Debug the entire MBTiles
        decoded = mvt_debugger.get_decoded_tiles()
        layers_dict = mvt_debugger.get_digested_layers_dict(decoded)
    elif tile is not None and zoom is None:
        # Debug a tile
        decoded = mvt_debugger.get_decoded_tile(tile)
        mvt_debugger.add_tile_layers_to_dict(decoded)
        layers_dict = mvt_debugger.layers_dict
    elif tile is None and zoom is not None:
        # Debug a zoom
        decoded = mvt_debugger.get_decoded_zoom(zoom)
        layers_dict = mvt_debugger.get_digested_layers_dict(decoded)

    spinner.stop()
    if layers_dict:
        rows = []
        for layer, info in layers_dict.items():
            f, v = info['n_features'], info['n_vertices']
            row = (layer, f, v)
            rows.append(row)

        fields = ('layer', 'n_features', 'n_vertices')
        mvt_printer.print(fields, rows)
