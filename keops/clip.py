"""Clip vector tiles from a MBTiles file using a given geoJSON file as a mask"""

import click

from .src.mvt_reader import MVTReader
from .src.mvt_clipper import MVTClipper


@click.command()
@click.argument('mbtiles', type=click.Path(exists=True))
@click.argument('geojson', type=click.Path(exists=True))
def clip(mbtiles, geojson):
    """
    Clip vector tiles in a MBTiles with a geoJSON file
    """
    mvt_reader = MVTReader(mbtiles)
    tiles = mvt_reader.get_decoded_tiles()
    mvt_clipper = MVTClipper(tiles, geojson)