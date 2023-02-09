from keops.src.utils import *


def test_decode_zxy_string():
    """

    :return:
    """
    assert decode_zxy_string('6/10/56') == ('6', '10', '56')

def test_geojson_checker_is_geojson():
    """
    """
    gj_checker = GeoJsonChecker('sample.shp')
    assert gj_checker._is_geojson() is False
