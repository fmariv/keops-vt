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

As this function uses a Docker image, you must have a running Docker version if you to use it. Also,
both the input and output MBTiles must be in the same directory, as it has to be mounted to
run the Docker image

"""


import os
import click
import docker

from .src.utils import get_shrink_command_options


@click.command(short_help='Reduce and simplify all features of all or any vector tiles in a MBTiles container. Docker required.')
@click.argument('input', type=click.Path(exists=True), required=True)
@click.argument('output', type=click.Path(), required=True)
@click.option('--extent', type=int, help='desired extent of the new layers [deault: 1024]')
@click.option('--precision', type=float, help='affects the level of simplification [deault: 1]')
@click.option('--shrink', type=int, help='maximal zoomlevel to apply the shrinking')
@click.option('--include', type=int, help='maximal zoomlevel to import untouched layers from [optional]')
def shrink(input, output, extent, precision, shrink, include):
    """Reduce and simplify all features of all or any vector tiles in a MBTiles container.

    Important:
        1. Docker required.
        2. Both input and output files must be in the same directory, as it has to be mounted
           to run Docker.

    $ keops shrink input.mbtiles output.mbtiles

    $ keops shrink --shrink 4 input.mbtiles output.mbtiles

    """
    # Input and output files must be different
    if input == output:
        click.echo('You must declare different input and output files')
        return

    # Get command options as string
    options = (extent, precision, shrink, include)
    command_options = get_shrink_command_options(options)

    # Get the input and output abspaths
    input_dir, output_dir = os.path.abspath(os.path.dirname(input)), os.path.abspath(os.path.dirname(output))
    if input_dir != output_dir:
        click.echo('Both input and output MBTiles must be in the same directory')
        return

    # Get the input and output file names
    input_file, output_file = os.path.basename(input), os.path.basename(output)
    # By default, the bind is /opt/data
    shrink_command = f'tileshrink {command_options} /opt/data/{input_file} /opt/data/{output_file}'
    shrink_mount = {input_dir: {'bind': '/opt/data', 'mode': 'rw'}}

    # Run the tileshrink
    client = docker.from_env()
    container_name = 'keops-tileshrink'
    image_name = "franmartin/tileshrink:latest"
    container = client.containers.run(image_name,
                                      name=container_name,
                                      volumes=shrink_mount,
                                      command=shrink_command,
                                      detach=True,
                                      remove=True)

    logs = container.logs(stream=True)
    for line in logs:
        click.echo(line.strip())
