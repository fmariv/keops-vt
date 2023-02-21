import sqlite3
import gzip
import mapbox_vector_tile

from click import echo
from .utils import decode_zxy_string


TILE_SIZE_LIMIT = 500


class MVTReader:
    """Read a MBTiles file and return its data, decoded or not"""

    def __init__(self, mbtiles: str):
        self.mbtiles = mbtiles
        self.conn = self._get_conn()
        self.cur = self._get_cur()

    def _get_conn(self):
        """

        :return:
        """
        conn = self._create_connection(self.mbtiles)
        return conn

    def _get_cur(self):
        """

        :return:
        """
        return self.conn.cursor()

    def _query(self, sql_query):
        """

        :param sql_query:
        :return:
        """
        try:
            self.cur.row_factory = lambda cursor, row: row[0]
            self.cur.execute(sql_query)
            response = self.cur.fetchall()
            self.cur.row_factory = None
            self.conn.close()
        except Exception as e:
            echo(e)
            return

        return response

    def get_tile_size(self, zxy: str) -> float:
        """

        :param zxy:
        :return:
        """
        z, x, y = decode_zxy_string(zxy)
        tile_exists = self._check_tile_exists(z, x, y)

        if not tile_exists:
            self.conn.close()
            print(f'Error: The given tile at {zxy} does not exists in the MBTiles file')
            return 0

        # Get the size in KB
        query = f'SELECT length(tile_data) as size FROM tiles WHERE zoom_level={z} AND tile_column={x} AND tile_row={y}'
        tile_size = self._query(query)[0] * 0.001
        tile_size = round(tile_size, 3)

        return tile_size

    def get_zoom_size(self, z: int) -> float:
        """

        :param z:
        :return:
        """
        zoom_exists = self._check_zoom_exists(z)

        if not zoom_exists:
            self.conn.close()
            print(f'Error: The given zoom {z} does not exists in the MBTiles file')
            return 0

        # Sum the response and get the size in KB
        query = f'SELECT length(tile_data) as size FROM tiles WHERE zoom_level={z}'
        zoom_size = sum(self._query(query)) * 0.001
        zoom_size = round(zoom_size, 3)

        return zoom_size

    def get_tiles(self):
        """
        Query and return the features of all the tiles in the MBTiles

        Estructure of the tiles
        for tile in tiles:
            tile[0] = zoom
            tile[1] = x column
            tile[2] = y column
            tile[3] = encoded data

        :return: tiles: tuple containing data in the MBTiles
        """
        query = 'SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles'

        tiles = self._query(query)

        if tiles:
            return tiles
        else:
            echo('There is no data in the MBTiles')
            return

    def get_big_tiles(self):
        """
        Query and return the features of the big tiles in the MBTiles

        Estructure of the tiles
        for tile in tiles:
            tile[0] = zoom
            tile[1] = x column
            tile[2] = y column
            tile[3] = encoded data

        :return: tiles: tuple containing data in the MBTiles
        """
        query = f'SELECT zoom_level, tile_column, tile_row, tile_data, length(tile_data) as size FROM tiles WHERE length(tile_data) > {TILE_SIZE_LIMIT * 1024} ORDER BY zoom_level, tile_column, tile_row ASC'

        tiles = self._query(query)

        if tiles:
            return tiles
        else:
            echo('There is no data or at least not too big tiles in the MBTiles')
            return

    def get_decoded_tiles(self, size_limit=False) -> list:
        """
        Query, decode and return the features of the MBTiles

        Estructure of the decoded tiles
        for tile in tiles:
            tile[0] = zoom
            tile[1] = x column
            tile[2] = y column
            tile[3] = decoded data
            for layer, layer_data in tile[3].items():
                layer = layer name
                layer_data = geojson

        :param: size_limit: indicates if the there is a size constraint
        in the query
        :return: tiles: tuple containing decoded data in the MBTiles
        """
        decoded_tiles = []
        tiles = self.get_tiles() if size_limit else self.get_big_tiles()

        if tiles:
            for tile in tiles:
                decoded_tile_data = self._decode_tile_data(tile)
                decoded_tile = [tile[0], tile[1], tile[2], decoded_tile_data]
                decoded_tiles.append(decoded_tile)
        else:
            echo('There is no data or at least not too big tiles in the MBTiles')
            return

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
            echo(e)

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
    def _get_tile_zxy_string(tile: tuple) -> str:
        """
        Get the zoom level, tile column and tile row
        in string format
        :param: tile: Vector tile object
        :return: String with the zoom level, tile column
        and tile row
        """
        zxy = f'{tile[0]}/{tile[1]}/{tile[2]}'
        return zxy

    @staticmethod
    def _get_tile_data(tile: tuple) -> str:
        """
        Get decompressed tile data
        :param: tile: Vector tile object
        :return: Decompressed tile data
        """
        return gzip.decompress(tile[3])

    def _decode_tile_data(self, tile: tuple) -> dict:
        """
        Get the decoded tile data
        :param: tile_data: Data in the vector tile
        :return: Decoded tile data
        """
        encoded_tile_data = self._get_tile_data(tile)
        try:
            return mapbox_vector_tile.decode(encoded_tile_data)
        except Exception as e:
            echo(e)

    def _check_tile_exists(self, z: int, x: int, y: int) -> bool:
        """

        :param zxy:
        :return:
        """
        query = f'SELECT * from tiles WHERE zoom_level={z} AND tile_column={x} AND tile_row={y};'

        try:
            self.cur.execute(query)
            result = self.cur.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def _check_zoom_exists(self, zoom_level: int) -> bool:
        """

        :param zoom_level:
        :return:
        """
        query = f'SELECT * from tiles WHERE zoom_level={zoom_level} LIMIT 1'

        try:
            self.cur.execute(query)
            result = self.cur.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
