from keops.src.mvt_reader import MVTReader

MBTILES = 'tests/fixtures/sample.mbtiles'

reader = MVTReader(MBTILES)


def test_check_tile_exists():
    """

    :return:
    """
    tile_exists = reader._check_tile_exists('8', '128', '160')

    assert tile_exists is True


def test_check_zoom_exists():
    """

    :return:
    """
    zoom_exists = reader._check_zoom_exists('16')

    assert zoom_exists is False


def test_get_tile_size():
    """

    :return:
    """
    tile_size = reader.get_tile_size('8/128/160')

    assert tile_size == 152.888


def test_get_zoom_size():
    """

    :return:
    """
    zoom_size = reader.get_zoom_size('8')

    assert zoom_size == 696.647
