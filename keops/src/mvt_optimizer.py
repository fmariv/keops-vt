import sqlite3
import gzip
import mapbox_vector_tile


def get_tiles(mbtiles_path):
    """
    """
    print(mbtiles_path)
    conn = create_connection(mbtiles_path)
    cur = conn.cursor()

    try:
        cur.execute(f'SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles')
        tiles = cur.fetchall()
    except Exception as e:
        print(e)

    return tiles


def create_connection(db_file):
    """
    Create a database connection to the SQLite database
    specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def get_tile_zxy(tile):
    """
    Get the zoom level, tile column and 
    tile row
    :param: tile: Vector tile object
    :return: Zoom level, tile column and tile row
    """
    return (tile[0], tile[1], tile[2])


def get_tile_zxy_string(tile):
    """
    Get the zoom level, tile column and tile row
    in string format
    :param: tile: Vector tile object
    :return: String with the zoom level, tile column
    and tile row
    """
    return (f'{tile[0]}/{tile[1]}/{tile[2]}')


def get_tile_data(tile):
    """
    Get decompressed tile data
    :param: tile: Vector tile object
    :return: Decompressed tile data
    """
    return gzip.decompress(tile[3])


def get_decoded_tile_data(tile_data):
    """
    Get the decoded tile data
    :param: tile_data: Data in the vector tile
    :return: Decoded tile data
    """
    try:
        return mapbox_vector_tile.decode(tile_data)
    except Exception as e:
        print(e)


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


if __name__ == '__main__':
    mbtiles = '/dev/data/input.mbtiles'
    tiles = get_tiles(mbtiles)
    for tile in tiles:
        zxy = get_tile_zxy_string(tile)
        tile_data = get_tile_data(tile)
        decoded_tile_data = get_decoded_tile_data(tile_data)
        for layer, layer_data in decoded_tile_data.items():
            print(layer)
            print("-------------------")
            print(layer_data)
        break
