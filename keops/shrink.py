"""Reduce and simplify all features of all or any vector tiles in an MBTiles container"""

"""
Disclaimer

The merit of this module belongs entirely to @rastapasta, as the unique developer of tileshrink,
and @ooZberg, as the person who wrapped it in a Docker image in order to use it without worrying
about the Node.js version. What I have done is creating a backup of the Docker image and 
wrapping it again in this package, so it can be used in a focused environment.

Check them GitHubs here and give kudos to them!
@rastapasta: https://github.com/rastapasta
@ooZberg: https://github.com/ooZberg


Important

As this function uses a Docker image, you must have a running Docker version if you to use it

"""


import click
import docker


@click.command(short_help='Reduce and simplify all features of all or any vector tiles in an MBTiles container')
@click.argument('input', type=click.Path(exists=True), required=True)
@click.argument('output', type=click.Path(), required=True)
@click.option('--extent', type=int, help='desired extent of the new layers [deault: 1024]')
@click.option('--precision', type=float, help='affects the level of simplification [deault: 1]')
@click.option('--shrink', type=int, help='maximal zoomlevel to apply the shrinking')
@click.option('--include', type=int, help='maximal zoomlevel to import untouched layers from [optional]')
def shrink(input, output, extent, precision, shrink, include):
    """Reduce and simplify all features of all or any vector tiles in an MBTiles container.

    Important: you do need a running Docker version if you want to use this function

    $ keops shrink input.mbtiles output.mbtiles

    """
    client = docker.from_env()
    client.containers.run("oozberg/tileshrink", name='keops-tileshrink', command="echo hello world")
    container = client.containers.get('keops-tileshrink')
    try:
        for line in container.logs(stream=True):
            print(line.strip())
    except:
        container.stop()

    container.stop()
