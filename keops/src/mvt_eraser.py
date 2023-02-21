from .mvt_reader import MVTReader

from .utils import decode_zxy_string


class MVTEraser(MVTReader):
    """Erase a tile in a MBTiles file"""

    def __init__(self, mbtiles: str):
        super().__init__(mbtiles)
        self.tile_table = self._get_tiles_table()

    def _get_tiles_table(self):
        """

        :return:
        """
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cur.row_factory = lambda cursor, row: row[0]

        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            self.cur.row_factory = None

            if 'tiles' in result:
                return 'tiles'
            elif 'map' in result and 'images' in result:
                return 'map'
            else:
                print('The are no tiles table in the MBTiles')
                return False
        except Exception as e:
            print(e)
            self.cur = None
            return False

    def _erase_tile_from_tiles(self, z, x, y):
        """

        :return:
        """
        query = f'DELETE FROM tiles WHERE zoom_level={z} AND tile_column={x} AND tile_row={y}'

        try:
            self.cur.execute(query)
            print(f'Tile in {z}/{x}/{y} erased successfully!')
            self.conn.close()
        except Exception as e:
            print(e)
            return False

    def _erase_tile_from_map_images(self, z, x, y):
        """

        :param z:
        :param x:
        :param y:
        :return:
        """
        try:
            query = f'SELECT tile_id FROM map WHERE zoom_level={z} AND tile_column={x} AND tile_row={y};'
            self.cur.execute(query)
            tile_id = self.cur.fetchone()
        except Exception as e:
            print(e)
            return False

        script = f"""
            DELETE FROM map WHERE tile_id={tile_id};
            DELETE FROM images WHERE tile_id={tile_id};
        """
        self.cur.executescript(script)

    def erase_tile(self, zxy):
        """

        :param z:
        :param x:
        :param y:
        :return:
        """
        if not self.tile_table:
            return False

        z, x, y = decode_zxy_string(zxy)
        tile_exists = self._check_tile_exists(z, x, y)
        if not tile_exists:
            self.conn.close()
            print(f'Error: The given tile at {zxy} does not exists in the MBTiles file')
            return False

        if self.tile_table == 'tiles':
            self._erase_tile_from_tiles(z, x, y)
        elif self.tile_table == 'map':
            self._erase_tile_from_map_images(z, x, y)
