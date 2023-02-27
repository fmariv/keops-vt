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


def test_zoom_is_valid():
    is_valid = zoom_is_valid('a')
    assert is_valid is False
