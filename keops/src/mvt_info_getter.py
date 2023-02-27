# Based on https://github.com/ibesora/vt-optimizer/blob/c1d480283bf5f9a132d9aed0ea705ebdaf76d161/src/core/Log.js
# TODO utilizar alguna libreria que haga tablas bonitas

class MVTInfoGetter:
    """ Class that logs the metrics of a MBTiles file"""

    def __init__(self):
        self.tiles_file = '././metrics/tiles.log'
        self.tile_layers_file = '././metrics/tiles_layers.log'

    def write_tiles_title(self):
        """
        Write the title in the tiles log
        """
        with open(self.tiles_file, 'w') as f:
            f.write('Vector Tile Summary\n')
            f.write('Zoom level   Tile column   Tile row   Tile size (KB)\n')
            f.write('----------   -----------   --------   --------------\n')
                                                           
    def write_tiles_layers_title(self):
        """
        Write the title in the tiles layers log
        """
        with open(self.tile_layers_file, 'w') as f:
            f.write('Tile Information\n')

    def write_tiles_list(self, tiles):
        """
        Write a the log file with the
        big vector tiles. The log includes
        zoom level, tile column, row column and 
        size in KB.
        :param: tiles: List with the position and size of every big tile
        """
        with open(self.tiles_file, 'a') as f:
            for tile in tiles:
                zxy = tile[0]
                size = tile[1]
                if len(str(zxy[0])) == 1:
                    f.write(f'{zxy[0]}            {zxy[1]}           {zxy[2]}        {size}\n')
                else:
                    f.write(f'{zxy[0]}           {zxy[1]}           {zxy[2]}        {size}\n')

    def write_tile_layers_overview(self, layers, file_object):
        """
        Write in the log file the overview layer information in a tile
        """
        n_layers, n_features, n_vertices = self.get_tile_layers_overview(layers)

        file_object.write(f'Layers in this tile: {n_layers}\n')
        file_object.write(f'Features in this tile: {n_features}\n')
        file_object.write(f'Vertices in this tile: {n_vertices}\n')

    def get_tile_layers_overview(self, layers):
        """
        Get the overview layer information in a tile
        """
        n_layers = len(layers) 
        n_features = self.get_number_features(layers) 
        n_vertices = self.get_number_vertices(layers)

        return n_layers, n_features, n_vertices

    def get_number_features(self, layers):
        """
        Get the number of features from a layer
        """
        n_features = 0
        for layer in layers:
            n_features += layer['n_features']

        return n_features

    def get_number_vertices(self, layers):
        """
        Get the number of vertices from a layer
        """
        n_vertices = 0
        for layer in layers:
            n_vertices += layer['n_vertices']

        return n_vertices

    def write_tiles_layers_list(self, data):
        """
        Write a log file with the data
        of every too big vector tile. This data includes:
        - OpenMapTiles layers in the tile
        - Number of features in the tile
        - Number of vertices in the tile
        :param: tiles: List a dict contianing data of every tile layers
        """
        with open(self.tile_layers_file, 'a') as f:
            for tile in data:
                tile_position = list(tile.keys())[0]
                tile_layers = list(tile.values())[0]

                f.write(f'Tile position: {tile_position}\n')
                self.write_tile_layers_overview(tile_layers, f)
                f.write('Layers:\n')
                f.write('Layer name            # of features   # of vertex\n')
                f.write('----------            -------------   -----------\n')
                for layer in tile_layers:
                    n_spaces_1 = 22-len(layer['layer'])
                    n_spaces_2 = 16-len(str(layer['n_features']))
                    f.write(f"{layer['layer']}{' ' * n_spaces_1}{layer['n_features']}{' ' * n_spaces_2}{layer['n_vertices']}\n")
                f.write('\n')


class MVTMetricsReader:

    def digest_decoded_tile_data(zxy, decoded_tile_data):
        """
        Digest the decoded tile data and return a digerible
        dictionary with it
        :param: zxy: Zoom level, tile column and row column
        of the vector tile
        :param: decoded_tile_data: Decoded data of the vector tile
        :return: digested_tile_data: Dictionary with the digested
        tile data
        """
        digested_tile_data = {}
        layer_list = []
        for layer, layer_data in decoded_tile_data.items():
            features = layer_data['features']
            n_features = len(features)
            n_vertices = 0
            for feature in features:
                n_vertices += len(feature['geometry']['coordinates'])
            layer_dict = {
                "layer": layer,
                "n_features": n_features,
                "n_vertices": n_vertices
            }
            layer_list.append(layer_dict)
        digested_tile_data[zxy] = layer_list

        return digested_tile_data

    def append_tile_data(tile):
        """
        Append the digested tile data in a list, in
        order to log it 
        :param tile: tile to get information from
        """
        zxy = get_tile_zxy_string(tile)
        tile_data = get_tile_data(tile)
        decoded_tile_data = get_decoded_tile_data(tile_data)
        digested_tile_data = digest_decoded_tile_data(zxy, decoded_tile_data)
