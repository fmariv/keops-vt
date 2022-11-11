import sqlite3
import gzip
import mapbox_vector_tile


TILE_SIZE_LIMIT = 500


class MVTReader():
    """Read a MBTiles file and return its data, decoded or not"""

    def __init__(self, mbtiles: str):
        self.mbtiles = mbtiles

    def get_tiles(self, size_limit=False):
        # TODO quit False argument, use another function instead
        """
        Query and return the features of the MBTiles
        :param: size_limit: indicates if the there is a size constraint
        in the query
        :return: tiles: tuple containing data in the MBTiles
        """
        conn = self._create_connection(self.mbtiles)
        cur = conn.cursor()

        if size_limit:
            query = f'SELECT zoom_level, tile_column, tile_row, tile_data, length(tile_data) as size FROM tiles WHERE length(tile_data) > {TILE_SIZE_LIMIT * 1024} ORDER BY zoom_level, tile_column, tile_row ASC'
        else:
            query = 'SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles'

        try:
            cur.execute(query)
            tiles = cur.fetchall()
            conn.close()
        except Exception as e:
            print(e)
            return

        if tiles:
            return tiles
        else:
            print('There is no data or at least not too big tiles')
            return

    def get_decoded_tiles(self, size_limit=False) -> list:
        """
        Query, decode and return the features of the MBTiles
        :param: size_limit: indicates if the there is a size constraint
        in the query
        :return: tiles: tuple containing decoded data in the MBTiles
        """
        decoded_tiles = []
        tiles = self.get_tiles(size_limit)

        if tiles:
            for tile in tiles:
                encoded_tile_data = self._get_tile_data(tile)
                decoded_tile_data = self._decode_tile_data(encoded_tile_data)
                decoded_tile = [tile[0], tile[1], tile[2], decoded_tile_data]
                decoded_tiles.append(decoded_tile)

            return decoded_tiles

    @staticmethod
    def _create_connection(db_file: str):
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

    @staticmethod
    def _get_tile_zxy(tile: tuple) -> tuple:
        """
        Get the zoom level, tile column and 
        tile row
        :param: tile: Vector tile object
        :return: Zoom level, tile column and tile row
        """
        zxy = (tile[0], tile[1], tile[2])
        return zxy

    @staticmethod
    def _get_tile_zxy_string(tile: tuple) -> tuple:
        """
        Get the zoom level, tile column and tile row
        in string format
        :param: tile: Vector tile object
        :return: String with the zoom level, tile column
        and tile row
        """
        zxy = (f'{tile[0]}/{tile[1]}/{tile[2]}')
        return zxy

    @staticmethod
    def _get_tile_data(tile: tuple) -> str:
        """
        Get decompressed tile data
        :param: tile: Vector tile object
        :return: Decompressed tile data
        """
        return gzip.decompress(tile[3])

    @staticmethod
    def _decode_tile_data(tile_data: str) -> dict:
        """
        Get the decoded tile data
        :param: tile_data: Data in the vector tile
        :return: Decoded tile data
        """
        try:
            return mapbox_vector_tile.decode(tile_data)
        except Exception as e:
            print(e)
