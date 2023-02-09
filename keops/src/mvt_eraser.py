from .mvt_reader import MVTReader

from .utils import decode_zxy_string


class MVTEraser(MVTReader):
    """Erase a tile in a MBTiles file"""

    def __init__(self, mbtiles: str):
        super().__init__(mbtiles)

    def _check_tile_exists(self, z, x, y):
        """

        :param zxy:
        :return:
        """
        query = f'SELECT * from tiles WHERE zoom_level={z} AND tile_column={x} AND tile_row={y}'

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

    def erase_tile(self, zxy):
        """

        :param z:
        :param x:
        :param y:
        :return:
        """
        # TODO check if tiles is a view, remove map 
        # TODO Rebuild indexes?
        z, x, y = decode_zxy_string(zxy)
        tile_exists = self._check_tile_exists(z, x, y)
        if not tile_exists:
            self.conn.close()
            print(f'Error: The given tile at {zxy} does not exists in the MBTiles file')
            return False

        query = f'DELETE FROM tiles WHERE zoom_level={z} AND tile_column={x} AND tile_row={y}'

        try:
            self.cur.execute(query)
            print(f'Tile in {zxy} erased successfully!')
            self.conn.close()
        except Exception as e:
            print(e)
            return False
