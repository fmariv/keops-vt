"""Clip vector tiles from a MBTiles file using a given geoJSON file as a mask"""

import click
import geopandas as gpd
import json

from shapely.geometry import Polygon, LineString, Point, MultiPolygon, MultiLineString, shape

from .utils import translate_geojson_crs

GEOMETRY_DICT = {
    'Polygon': Polygon,
    'LineString': LineString,
    'Point': Point,
    'MultiPolygon': MultiPolygon,
    'MultiLineString': MultiLineString
}


class MVTClipper:
    
    def __init__(self, geojson_mask: str):
        self.geojson_mask_shape = self._set_geojson_mask(geojson_mask)

    def _set_geojson_mask(self, geojson_mask):
        """

        :param geojson_mask:
        :return:
        """
        geojson_mask_gdf = gpd.read_file(geojson_mask)

        # Check if the GeoJSON CRS is in Google Mercator
        # If not, translate
        if not geojson_mask_gdf.crs == 'epsg:3857':
            geojson_mask_gdf = translate_geojson_crs(geojson_mask_gdf)

        geojson_mask_shape = self._geodataframe_to_shapely(geojson_mask_gdf)

        return geojson_mask_shape

    @staticmethod
    def _geodataframe_to_shapely(geodataframe):
        """
        Convert GeoDataFrame to Shapely Polygon object
        :param geodataframe:
        :return:
        """
        geojson_str = geodataframe.to_json()
        geojson_dict = json.loads(geojson_str)
        mask = geojson_dict['features'][0]
        mask_shape = shape(mask['geometry'])

        return mask_shape

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
            x, y, z = tile[0], tile[1], tile[2]
            tile_intersects_mask = False
            layer_data = tile[3]
            for layer, data in layer_data.items():
                feature = data['features'][0]
                geometry = feature['geometry']
                # Get the geometry type and coordinates to
                # create a shapely object
                geometry_type, coordinates = geometry['type'], geometry['coordinates']
                # Get shapely geometry type with the GEOMETRY_DICT
                # and create a shapely object
                feature_shape = GEOMETRY_DICT[geometry_type](coordinates)
                if feature_shape.intersects(self.geojson_mask_shape):
                    tile_intersects_mask = True if not tile_intersects_mask else True

        return None
