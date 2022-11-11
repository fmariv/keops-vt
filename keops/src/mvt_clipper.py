"""Clip vector tiles from a MBTiles file using a given geoJSON file as a mask"""

import geopandas as gpd


class MVTClipper:
    
    def __init__(self, geojson_mask: str):
        self.geojson_mask = geojson_mask
