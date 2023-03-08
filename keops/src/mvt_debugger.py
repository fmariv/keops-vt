from .mvt_reader import MVTReader


class MVTDebugger(MVTReader):
    """Debug a MBTiles file. Get info related with layers and their features of a given tile or zoom level in a MBTiles file"""

    def __init__(self, mbtiles: str):
        super().__init__(mbtiles)
        self.tile_table = self._get_tiles_table()

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
