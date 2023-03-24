import click
import re

GOOGLE_MERCATOR = 'EPSG:3857'


def decode_zxy_string(tile: str) -> tuple:
    """
    Decode a string with format z/x/y and return every parameter as an integer
    :param tile: Tile position, as z/x/y
    :return: Decoded tile position, with every parameter as an integer
    """
    zxy = tile.split('/')
    z, x, y = int(zxy[0]), int(zxy[1]), int(zxy[2])
    return z, x, y


def zxy_string_is_valid(tile: str) -> bool:
    """
    Check if a given tile position, with format z/x/y, is valid
    :param tile: Tile position, as z/x/y
    :return: Return a boolean that indicates if the given tile position is valid
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


def tile_zoom_are_valid(zoom: int, tile: str) -> bool:
    """
    Check if the user has given a tile position or a zoom, but not both at the same time
    or none of them
    :param tile: Tile position, as z/x/y
    :param zoom: Zoom, as integer
    :return: Return a boolean that indicates if the user has given the inputs correctly
    """
    if zoom is None and tile is None:
        click.echo('You have to give at least a tile or a zoom level')
        return False
    if zoom is not None and tile is not None:
        click.echo('You only have to give a tile or a zoom level, not both of them')
        return False

    if zxy_string_is_valid(tile) and type(zoom) == int:
        return True
    else:
        return False


def mbtiles_is_valid(mbtiles: str) -> bool:
    """
    Check if a given file is a MBTiles, which is SQLite database
    :param mbtiles: The file to check if it is a valid MBTiles
    :return: Return a Boolean that indicates if the file is a valid MBTiles
    """
    # TODO
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
