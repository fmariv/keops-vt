# Keops: tile pyramid management

Keops is a CLI tool that allows you to apply some logic to vector tiles in a MBTiles file, such as removing or getting the size of a given tile, obtaining the vector layers that conform the MBTiles or shrinking the vector data, in order to reduce the data size.

## Installation

Keops needs Python 3.7 or higher. The recommended way to install it is via [pip](https://pypi.org/project/keops-tiles/).

``` 
pip install keops-vt
```

If you want to run the ```shrink``` command you also need [Docker](https://www.docker.com/).

## Commands

The usage of Keops is pretty simple and straigthforward. If you want to check functions, simply execute ```keops``` or ```keops --help``` in your bash.

````
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
````

### Erase

The ``erase`` command drops a tile in a MBTiles file.

```
keops erase input.mbtiles 10/56/65
```

### Size

The ```size``` command gets the size in KB of a given tile or given zoom level.

```
keops size --zoom 10 input.mbtiles
keops size --tile 10/56/65 input.mbtiles
```

### Shrink

The ```shrink``` command reduces and simplifies all features of all or any vector tiles in a MBTiles container.

```
keops shrink --shrink 4 input.mbtiles output.mbtiles
```

#### Disclaimer

The merit of this module belongs entirely to [rastapasta](https://github.com/rastapasta), as the unique developer of tileshrink,
and [ooZberg](https://github.com/ooZberg), as the person who wrapped it in a Docker image in order to use it without worrying
about the Node.js version. What I have done is creating a backup of the Docker image and 
wrapping it again in this package, so it can be used in a focused environment.

Give kudos to them!

#### Important

As this function uses a Docker image, you must have a running Docker version if you to use it. Also,
both the input and output MBTiles must be in the same directory, as it has to be mounted to
run the Docker image

### Info

The ```ìnfo``` command gets info related with layers and their features of a given tile or zoom level in a MBTiles file.

```
keops info --zoom 10 input.mbtiles
keops info --tile 10/56/65 input.mbtiles
```

### Debug

The ```debug``` command gets info related with layers and their features in a given MBTiles.

```
$ keops debug input.mbtiles
$ keops debug --zoom 10 input.mbtiles
$ keops debug --tile 10/56/65 input.mbtiles
```