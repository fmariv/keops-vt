# Keops
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#wip)
![CI](https://github.com/fmariv/keops-vt/actions/workflows/test_lint.yaml/badge.svg)

<p align="center">
    <img src="favicon.png" alt="Keops logo">
</p>

Keops is a CLI tool that allows you to apply some logic to vector tiles in a MBTiles file, such as removing or getting the size of a given tile, obtaining the vector layers that conform the MBTiles or shrinking the vector data, in order to reduce the data size.

Read the full documentation for more details: [keops.franmartin.es](https://keops.franmartin.es/).

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

Keops have some more functionalities. To check them, simply execute ```keops``` or ```keops --help``` in your bash.

```bash
Usage: keops [OPTIONS] COMMAND [ARGS]...

  Keops command line interface

Options:
  --help  Show this message and exit.
 
Commands:
  debug   Debug a MBTiles file: get info related with layers and their
          features in a given MBTiles
  erase   Erase a tile in a MBTiles file
  info    Extract and print the metadata info from a MBTiles file
  shrink  Reduce and simplify all features of all or any vector tiles in a
          MBTiles container. Docker required.
  size    Get the size of a given tile or zoom level in a MBTiles file


```

## Roadmap

If you are interested on the roadmap of the project, check the [ROADMAP](ROADMAP.md) file.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Credits

The merit of the shrink module belongs entirely to [rastapasta](https://github.com/rastapasta/tileshrink), as the unique developer of tileshrink,
and [ooZberg](https://github.com/ooZberg), as the person who wrapped it in a Docker image in order to use it without worrying
about the Node.js version. What I have done is creating a backup of the Docker image and 
wrapping it again in this package, so it can be used in a focused environment.