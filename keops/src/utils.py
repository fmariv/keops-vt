import geopandas as gpd

GOOGLE_MERCATOR = 'EPSG:3857'


def check_geojson_is_valid(geojson_mask):
    """

    :return:
    """
    # Check file is a geoJSON
    if not geojson_mask.endswith('.geojson'):
        print('Mask file is not a geoJSON')
        return False

    # Check geoJSON is valid
    geojson_df = gpd.read_file(geojson_mask)
    if not geojson_df.is_valid():
        print('GeoJSON file is not valid')
        return False

    # TODO check geoJSON bounds with MBTiles

    return True


def translate_geojson_crs(geojson_mask):
    """

    :param geojson_mask: Geopandas GeoDataFrame of the geoJSON mask file
    :return:
    """
    return geojson_mask.to_crs(GOOGLE_MERCATOR)
