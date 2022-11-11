"""Clip vector tiles from a MBTiles file using a given geoJSON file as a mask"""

import geopandas as gpd

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

    def clip_mbtiles(self, tiles):
        """

        :param tiles:
        :return:
        """
        return tiles
