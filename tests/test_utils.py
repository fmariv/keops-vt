from keops.src.utils import *


def test_decode_zxy_string():
    """
    Test the decode_zxy_string function from keops.src.utils
    """
    assert decode_zxy_string('6/10/56') == (6, 10, 56)


def test_zxy_string_is_valid():
    """
    Test the zxy_string_is_valid function from keops.src.utils
    """
    is_valid = zxy_string_is_valid('a/2/12')
    assert is_valid is False


def test_tile_zoom_are_valid():
    """
    Test the tile_zoom_are_valid function from keops.src.utils
    """
    is_valid = tile_zoom_are_valid(None, 'a/2/12')
    assert is_valid is False


def test_get_shrink_command_options():
    """
    Test the get_shrink_command_options function from keops.src.utils
    """
    expected = '--precision 2 --include 10'
    options = (None, 2, None, 10)
    result = get_shrink_command_options(options)
    assert expected == result


def test_mbtiles_is_valid():
    """
    Test the mbtiles_is_valid function from keops.src.utils
    """
    is_valid = mbtiles_is_valid('test/fixtures/empty.mbtiles')
    assert is_valid is False
