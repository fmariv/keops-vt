from keops.src.utils import *


def test_decode_zxy_string():
    """

    :return:
    """
    assert decode_zxy_string('6/10/56') == (6, 10, 56)


def test_geojson_checker_is_geojson():
    """
    """
    gj_checker = GeoJsonChecker('sample.shp')
    assert gj_checker._is_geojson() is False


def test_zxy_string_is_valid():
    is_valid = zxy_string_is_valid('a/2/12')
    assert is_valid is False


def test_tile_zoom_are_valid():
    is_valid = tile_zoom_are_valid('a', 'a/2/12')
    assert is_valid is False


def test_get_shrink_command_options():
    expected = '--precision 2 --include 10'
    options = (None, 2, None, 10)
    result = get_shrink_command_options(options)
    assert expected == result
