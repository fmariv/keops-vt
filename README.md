# Keops
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![CI](https://github.com/fmariv/keops-vt/actions/workflows/test_lint.yaml/badge.svg)

<p align="center">
    <img src="favicon.png" alt="Keops logo">
</p>

Keops is a CLI tool that allows you to apply some logic to vector tiles in an MBTiles, such as clipping by a GeoJSON mask, size optimization by removing unnecessary feautures in a given GL style, and much more.

Read the documentation for more details: [keops.franmartin.es](https://keops.franmartin.es/).


_Still in development! The package is not stable yet_

## Installation

Keops needs Python 3.7 or higher. The recommended way to install it is via [pip](https://pypi.org/project/keops-tiles/).

``` 
pip install keops-vt
```

If you want to run the ```shrink``` command you also need [Docker](https://www.docker.com/).

## CLI Usage

The usage is pretty simple and straigthforward. For instance, if you want to drop a given tile in a MBTiles:

```bash
keops erase input.mbtiles 6/10/23
```

Keops have some more functionalities. To check them, simply execute ```keops``` or ```keops --help``` in your bash

```bash
Usage: keops [OPTIONS] COMMAND [ARGS]...

  Keops command line interface

Options:
  --help  Show this message and exit.
 
Commands:
  clip    Clip vector tiles to given geoJSON
  erase   Erase a tile in a MBTiles file
  info    Get info related with layers and their features of a given tile or
          zoom level in a MBTiles file
  shrink  Reduce and simplify all features of all or any vector tiles in a
          MBTiles container. Docker required.
  size    Get the size of a given tile or zoom level in a MBTiles file

```

## Author

Fran Martín

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.