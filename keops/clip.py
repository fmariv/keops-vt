"""Clip vector tiles from a MBTiles file using a given geoJSON file as a mask"""

import click

from .src.mvt_reader import MVTReader
from .src.mvt_clipper import MVTClipper
from .src.utils import GeoJsonChecker


@click.command(short_help='Clip vector tiles to given geoJSON')
@click.argument('mbtiles', type=click.Path(exists=True), required=True)
@click.argument('geojson', type=click.Path(exists=True), required=True)
def clip(mbtiles, geojson):
    """Clips vector tiles in a MBTiles using a geoJSON file as a mask.

    $ keops clip input.mbtiles bounds.geojson

    """
    gj_checker = GeoJsonChecker(geojson)
    geojson_is_valid = gj_checker.check_geojson_is_valid()
    if not geojson_is_valid:
        return

    mvt_reader = MVTReader(mbtiles)
    tiles = mvt_reader.get_decoded_tiles()
    mvt_clipper = MVTClipper(geojson)
    clipped_tiles = mvt_clipper.clip_mbtiles(tiles)
