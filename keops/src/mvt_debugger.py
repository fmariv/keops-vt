import click

from .mvt_reader import MVTReader


class MVTDebugger(MVTReader):
    """
    Debug a MBTiles file. Get info related with layers and their
    features of a given tile or zoom level in a MBTiles file
    """

    def __init__(self, mbtiles: str):
        super().__init__(mbtiles)
        self.layers_dict = {}

    @staticmethod
    def digest_decoded_tile_data(decoded_tile_data: dict) -> dict:
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

    def get_digested_layers_dict(self, decoded_tiles: list) -> list or None:
        """

        :param decoded_tiles:
        :return:
        """
        if decoded_tiles:
            # Get a dict with the number of features and vertices of every layer
            for tile in decoded_tiles:
                self.add_tile_layers_to_dict(tile)
            return self.layers_dict
        else:
            click.echo('No data returned')   # TODO
            return

    def add_tile_layers_to_dict(self, tile: list):
        """

        :param tile:
        :return:
        """
        data = tile[3]
        digested_data = self.digest_decoded_tile_data(data)
        for layer, info in digested_data.items():
            if layer in self.layers_dict:
                # Sum the number of features and vertices to the existing
                # Get the existing data to sum to the new one
                existing_layer_data = self.layers_dict.get(layer)
                existing_n_features = existing_layer_data['n_features']
                existing_n_vertices = existing_layer_data['n_vertices']
                # Get the new data
                new_n_features = existing_n_features + info['n_features']
                new_n_vertices = existing_n_vertices + info['n_vertices']
                # Update the key
                self.layers_dict[layer] = {'n_features': new_n_features, 'n_vertices': new_n_vertices}
            else:
                # Set the new layer as features and vertices
                self.layers_dict[layer] = {'n_features': info['n_features'], 'n_vertices': info['n_vertices']}
