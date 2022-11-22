"""Clip vector tiles from a MBTiles file using a given geoJSON file as a mask"""

import geopandas as gpd

from shapely.geometry import LineString
from shapely import wkt

from .utils import translate_geojson_crs


class MVTClipper:
    
    def __init__(self, geojson_mask: str):
        self.geojson_mask = self._set_geojson_mask(geojson_mask)

    @staticmethod
    def _set_geojson_mask(geojson_mask):
        """

        :param geojson_mask:
        :return:
        """
        geojson_mask_gdf = gpd.read_file(geojson_mask)

        if not geojson_mask_gdf.crs == 'epsg:3857':
            geojson_mask_gdf = translate_geojson_crs(geojson_mask_gdf)

        return geojson_mask_gdf

    def _tile_intersects_mask(self, tile):
        """

        :param tile:
        :return:
        """
        pass

    def clip_mbtiles(self, tiles):
        """

        :param tiles:
        :return:
        """
        for tile in tiles:
            layer_data = tile[3]
            for layer, data in layer_data.items():
                features = data['features']
        return tiles
