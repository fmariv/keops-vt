"""Clip vector tiles from a MBTiles file using a given geoJSON file as a mask"""

import click

from .mvt_reader import MVTReader


class MVTClipper:
    
    def __init__(self, tiles: str, mask_file: str):
        self.tiles = tiles
        self.mask_file = mask_file


if __name__ == '__main__':
    pass