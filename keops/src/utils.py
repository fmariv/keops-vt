import click
import re

from halo import Halo

GOOGLE_MERCATOR = 'EPSG:3857'


def decode_zxy_string(tile: str) -> tuple:
    """
    Decode a string with format z/x/y and return every parameter as an integer

    :param tile: tile position, as z/x/y
    :return: decoded tile position, with every parameter as an integer
    """
    zxy = tile.split('/')
    z, x, y = int(zxy[0]), int(zxy[1]), int(zxy[2])
    return z, x, y


def zxy_string_is_valid(tile: str) -> bool:
    """
    Check if a given tile position, with format z/x/y, is valid

    :param tile: tile position, as z/x/y
    :return: boolean that indicates if the given tile position is valid
    """
    zxy = tile.split('/')
    if len(zxy) != 3:
        click.echo(f'Tile format {tile} is not valid. It must follows the format z/x/y')
        return False
    for i in zxy:
        if re.search('[a-zA-Z]', i) is not None:
            click.echo('The given tile contains letters. It must follows the format z/x/y ONLY with integers')
            return False
    return True


def tile_zoom_are_valid(zoom: int or None, tile: str or None) -> bool:
    """
    Check if the user has given a tile position or a zoom, but not both at the same time
    or none of them

    :param tile: tile position, as z/x/y
    :param zoom: zoom, as integer
    :return: boolean that indicates if the user has given the inputs correctly
    """
    if zoom is None and tile is None:
        click.echo('You have to give at least a tile or a zoom level')
        return False
    elif zoom is not None and tile is not None:
        click.echo('You only have to give a tile or a zoom level, not both of them')
        return False
    elif zoom is None and tile is not None:
        return True if zxy_string_is_valid(tile) else False
    elif zoom is not None and tile is None:
        return True if type(zoom) == int else False


def mbtiles_is_valid(mbtiles: str) -> bool:
    """
    Check if a given file is a MBTiles, which is SQLite database

    :param mbtiles: file to check if is a valid MBTiles
    :return: boolean that indicates if the file is a valid MBTiles
    """
    from os.path import isfile, getsize

    error_message = '[>] The given MBTiles is not a valid SQLite database'
    if not isfile(mbtiles):
        click.echo(error_message)
        return False
    if getsize(mbtiles) < 100:  # SQLite database file header is 100 bytes
        click.echo(error_message)
        return False
    with open(mbtiles, 'rb') as fd:
        header = fd.read(100)

    if header[:16] != b'SQLite format 3\x00':
        click.echo(error_message)
        return False

    return True


def get_shrink_command_options(options: tuple) -> str:
    """
    Wrap the options given to the shrink command into a single string with them,
    in order to pass it to the tileshrink Docker
    :return: Return a string containing all the given commands
    """
    command_options = ''
    options_flags = {0: '--extent', 1: '--precision', 2: '--shrink', 3: '--include'}
    for option in options:
        if option is not None:
            i = options.index(option)
            flag = options_flags[i]
            option_command = f'{flag} {option}'
            if not command_options:
                command_options = option_command
            else:
                command_options = f'{command_options} {option_command}'

    return command_options


def get_spinner(text: str) -> Halo:
    """
    Get a Halo spinner in 'dots' format. For Windows users, it defaults to 'line'.

    :param text: text to display while spinning
    :return: Halo spinner object
    """
    return Halo(text=text, spinner='dots', color='yellow')
