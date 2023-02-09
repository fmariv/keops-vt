import geopandas as gpd

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

        :param geojson_mask: Geopandas GeoDataFrame of the geoJSON mask file
        :return:
        """
        return self._geojson_mask.to_crs(GOOGLE_MERCATOR)


def decode_zxy_string(tile: str) -> tuple:
        """

        :param tile:
        :return:
        """
        zxy = tile.split('/')
        z, x, y = zxy[0], zxy[1], zxy[2]
        return z, x, y
