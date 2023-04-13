# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2023-04-13

### Added

- Feature to retrieve the tile info and metadata of a MBTiles.
- Feature to shrink (simplify) a MBTiles file. It uses [tileshrink](https://github.com/rastapasta/tileshrink).
- Feature to debug a MBTiles file, obtaining layers, number of features and number of vertices of each layer.

### Removed

- Setup.py file.

## [0.0.1] - 2023-02-20

### Added

- Feature to read a MBTiles, obtaining the required tiles from it.
- Feature to remove a given tile in a MBTiles.
- Feature to get the size of a given tile or zoom in a MBTiles.
