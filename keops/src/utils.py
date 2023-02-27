import click
import re

GOOGLE_MERCATOR = 'EPSG:3857'


class GeoJsonChecker:

    def __init__(self, geojson_mask):
        """
        """
        self._geojson_mask = geojson_mask

    def check_geojson_is_valid(self):
        """

        :return:
        """
        if not self._is_geojson:
            return False

        if not self._is_valid:
            pass

        if not self._is_polygon:
            pass

        if not self._bounds_intersect_mbtiles:
            pass

        return True

    def _is_geojson(self):
        """
        """
        if not self._geojson_mask.endswith('.geojson'):
            print('Mask file is not a geoJSON')
            return False

    def _is_valid(self):
        """
        """
        pass

    def _is_polygon(self):
        """
        """
        pass

    def _bounds_intersect_mbtiles(self):
        """
        """
        pass

    def translate_geojson_crs(self):
        """

        :return:
        """
        return self._geojson_mask.to_crs(GOOGLE_MERCATOR)


def decode_zxy_string(tile: str) -> tuple:
    """

    :param tile:
    :return:
    """
    zxy = tile.split('/')
    z, x, y = int(zxy[0]), int(zxy[1]), int(zxy[2])
    return z, x, y


def zxy_string_is_valid(tile: str) -> bool:
    """

    :param tile:
    :return:
    """
    zxy = tile.split('/')
    if len(zxy) != 3:
        click.echo(f'Tile format {tile} is not valid. It must follows the format z/x/y')
        return False
    for i in zxy:
        if re.search('[a-zA-Z]', i) is not None:
            click.echo('The given tile contains letters. It must follows the format z/x/y ONLY with integers')
            return False
    return True


def zoom_is_valid(zoom: any) -> bool:
    """

    :param zoom:
    :return:
    """
    try:
        int(zoom)
    except ValueError:
        click.echo('The given zoom level is not valid. It must be an integer')
        return False

    return True


def tile_zoom_are_valid(zoom: int, tile: str) -> bool:
    """

    :param tile:
    :param zoom:
    :return:
    """
    if zoom is None and tile is None:
        click.echo('You have to give at least a tile or a zoom level')
        return False
    if zoom is not None and tile is not None:
        click.echo('You only have to give a tile or a zoom level, not both of them')
        return False

    if zxy_string_is_valid(tile) and zoom_is_valid(zoom):
        return True
    else:
        return False


def mbtiles_is_valid(mbtiles):
    """

    :param mbtiles:
    :return:
    """
    return True
