import click
from prettytable import PrettyTable


class MVTPrinter:
    """Get info related with layers and their features of a given tile or zoom level in a MBTiles file"""

    def print_info(self, decoded_tile):
        """

        """
        # Get the tile data as a dict of pair:values as layer: {'n_features': n, 'n_vertices': n}
        decoded_tile_data = decoded_tile[3]
        layers = self._digest_decoded_tile_data(decoded_tile_data)

        # Print the tile info
        table = PrettyTable()
        table.field_names = ["Layer", "# of features", "# of vertices"]
        for layer, layer_info in layers.items():
            n_features = layer_info['n_features']
            n_vertices = layer_info['n_vertices']
            table.add_row([layer, n_features, n_vertices])

        click.echo(table)

    @staticmethod
    def _digest_decoded_tile_data(decoded_tile_data):
        """
        Digest the decoded tile data and return a digerible
        dictionary with it
        :param: decoded_tile: Decoded vector tile
        :return: digested_tile_data: Dictionary with the digested tile data
        """
        digested_tile_data = {}
        for layer, layer_data in decoded_tile_data.items():
            features = layer_data['features']
            n_features = len(features)
            n_vertices = 0
            for feature in features:
                n_vertices += len(feature['geometry']['coordinates'])
            layer_dict = {
                "n_features": n_features,
                "n_vertices": n_vertices
            }
            digested_tile_data[layer] = layer_dict

        return digested_tile_data
