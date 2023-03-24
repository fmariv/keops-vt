import sqlite3
import gzip
import mapbox_vector_tile
import click

from .utils import decode_zxy_string


TILE_SIZE_LIMIT = 500


class MVTReader:
    """Read a MBTiles file and return its data, decoded or not"""

    def __init__(self, mbtiles: str):
        self.mbtiles = mbtiles
        self.conn = self._get_conn()
        self.cur = self._get_cur()

    def _get_conn(self) -> sqlite3.connect:
        """
        Create the SQLite connection
        :return: SQlite connection
        """
        conn = self._create_connection(self.mbtiles)
        return conn

    def _get_cur(self) -> sqlite3.Cursor:
        """
        Get a SQLite connection cursor
        :return: SQLite cursor
        """
        return self.conn.cursor()

    def _query(self, sql_query: str, rows: bool = False, index: int = -1) -> list or None:
        """
        Run a given SQL query in the MBTiles file
        :param sql_query: SQL query to run in the MBTiles file
        :param rows: Boolean that indicates if the response must be a list with all the returned rows
        :param index: Integer that indicates which of the columns from the response have to be returned
        :return: Query response from the MBTiles file
        """
        try:
            if rows:
                if index >= 0:
                    self.cur.row_factory = lambda cursor, row: row[index]
                elif index < 0:
                    self.cur.row_factory = lambda cursor, row: row
            self.cur.execute(sql_query)
            response = self.cur.fetchall()
            self.cur.row_factory = None
            self.conn.close()
        except Exception as e:
            click.echo(e)
            return

        return response

    def get_tile_size(self, zxy: str) -> float:
        """
        Get the size in KB of a given tile in the MBTiles
        :param zxy: Tile position, as z/x/y
        :return: Size of the given tile, as KB
        """
        z, x, y = decode_zxy_string(zxy)
        tile_exists = self._check_tile_exists(z, x, y)

        if not tile_exists:
            self.conn.close()
            click.echo(f'Error: The given tile at {zxy} does not exists in the MBTiles file')
            return 0

        # Get the size in KB
        query = f'SELECT length(tile_data) as size FROM tiles WHERE zoom_level={z} AND tile_column={x} AND tile_row={y}'
        tile_size = self._query(query, True, 0)[0] * 0.001
        tile_size = round(tile_size, 3)

        return tile_size

    def get_zoom_size(self, z: int) -> float:
        """
        Get the size in KB of a given zoom in the MBTiles
        :param z: Zoom to get the zoom of
        :return: Size of the given zoom, as KB
        """
        zoom_exists = self._check_zoom_exists(z)

        if not zoom_exists:
            self.conn.close()
            click.echo(f'Error: The given zoom {z} does not exists in the MBTiles file')
            return 0

        # Sum the response and get the size in KB
        query = f'SELECT length(tile_data) as size FROM tiles WHERE zoom_level={z}'
        zoom_size = sum(self._query(query, True, 0)) * 0.001
        zoom_size = round(zoom_size, 3)

        return zoom_size

    def get_tile(self, zxy: str) -> list or None:
        """
        Get the data associated to a given tile, such as its zoom level, tile column, tile row
        and the encoded tile data as a Google proto buff
        :param zxy: Tile position, as z/x/y
        :return: Data associated to a given tile, with the encoded tile data
        """
        z, x, y = decode_zxy_string(zxy)
        tile_exists = self._check_tile_exists(z, x, y)

        if not tile_exists:
            self.conn.close()
            click.echo(f'Error: The given tile at {zxy} does not exists in the MBTiles file')
            return

        query = f'SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles WHERE zoom_level={z} AND tile_column={x} AND tile_row={y}'
        tile = self._query(query)[0]

        return tile

    def get_decoded_tile(self, zxy: str) -> list or None:
        """
        Get the data associated to a given tile, such as its zoom level, tile column, tile row
        and the decoded tile data as geoJSON
        :param zxy: Tile position, as z/x/y
        :return: Data associated to a given tile, with the decoded tile data
        """
        z, x, y = decode_zxy_string(zxy)
        tile_exists = self._check_tile_exists(z, x, y)

        if not tile_exists:
            self.conn.close()
            click.echo(f'Error: The given tile at {zxy} does not exists in the MBTiles file')
            return

        query = f'SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles WHERE zoom_level={z} AND tile_column={x} AND tile_row={y}'
        tile = self._query(query)[0]
        decoded_tile_data = self._decode_tile_data(tile)
        decoded_tile = [tile[0], tile[1], tile[2], decoded_tile_data]

        return decoded_tile

    def get_decoded_zoom(self, z: int) -> list or None:
        """
        Get the data associated to all the tiles in a given tile, such as them zoom level, tile column, tile row,
        and the decoded tile data as geoJSON
        :param z: Zoom to get the data of
        :return: Data associated to all the tiles in a given zoom, with the decoded tile data
        """
        zoom_exists = self._check_zoom_exists(z)

        if not zoom_exists:
            self.conn.close()
            click.echo(f'Error: The given zoom {z} does not exists in the MBTiles file')
            return

        # Get the decoded tiles from a given zoom
        query = f'SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles WHERE zoom_level={z}'
        zoom_tiles = self._query(query, True)
        decoded_zoom_data = []
        for tile in zoom_tiles:
            decoded_tile_data = self._decode_tile_data(tile)
            decoded_tile = [tile[0], tile[1], tile[2], decoded_tile_data]
            decoded_zoom_data.append(decoded_tile)

        return decoded_zoom_data

    def get_tiles(self) -> list or None:
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
            click.echo('There is no data in the MBTiles')
            return

    def get_big_tiles(self) -> list or None:
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

        tiles = self._query(query, True)

        if tiles:
            return tiles
        else:
            click.echo('There is no data or at least not too big tiles in the MBTiles')
            return

    def get_decoded_tiles(self, size_limit=False) -> list or None:
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
        tiles = self.get_tiles() if not size_limit else self.get_big_tiles()

        if tiles:
            for tile in tiles:
                decoded_tile_data = self._decode_tile_data(tile)
                decoded_tile = [tile[0], tile[1], tile[2], decoded_tile_data]
                decoded_tiles.append(decoded_tile)
        else:
            click.echo('There is no data or at least not too big tiles in the MBTiles')
            return

        return decoded_tiles

    def get_metadata(self) -> list or None:
        """
        Get the info from the metadata table in a MBTiles file
        :return: MBTiles metadata
        """
        query = 'SELECT name, value FROM metadata'

        metadata = self._query(query)

        if metadata:
            return metadata
        else:
            click.echo('There is no metadata in the MBTiles')
            return

    @staticmethod
    def _create_connection(db_file: str) -> sqlite3.connect:
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
            click.echo(e)

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
            click.echo(e)

    def _check_tile_exists(self, z: int, x: int, y: int) -> bool:
        """
        Check if a given tile exists in the MBTiles file
        :param: z: Zoom level of the given tile
        :param: x: Tile column of the given tile
        :param: y: Tile row of the given tile
        :return: Boolean that indicates if the given tile exists or not
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
            click.echo(e)
            return False

    def _check_zoom_exists(self, z: int) -> bool:
        """
        Check if a given zoom exists in a MBTiles file
        :param z: Zoom level to get if exists or not
        :return: Boolean that indicates if the given zoom exists or not
        """
        query = f'SELECT * from tiles WHERE zoom_level={z} LIMIT 1'

        try:
            self.cur.execute(query)
            result = self.cur.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as e:
            click.echo(e)
            return False
