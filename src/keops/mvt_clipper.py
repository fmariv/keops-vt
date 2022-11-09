"""Clip vector tiles from a MBTiles file using a given geoJSON file as a mask"""

import click

from mvt_reader import MVTReader


class MVTClipper:
    
    def __init__(self, tiles: str, mask_file: str):
        self.tiles = tiles
        self.mask_file = mask_file


@click.group()
def keops():
    """

    """
    pass

@keops.command()
@keops.argument('mbtiles', type=click.Path(exists=True))
@keops.argument('geojson', type=click.Path(exists=True))
def clip(mbtiles, geojson):
    """
    Clip vector tiles in a MBTiles with a geoJSON file
    """
    mvt_reader = MVTReader(mbtiles)
    tiles = mvt_reader.get_decoded_tiles()
    mvt_clipper = MVTClipper(tiles, geojson)


if __name__ == '__main__':
    passgg