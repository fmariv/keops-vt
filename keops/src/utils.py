import geopandas as gpd


def check_geojson_is_valid(geojson_mask):
    """

    :return:
    """
    # Check file is a geoJSON
    if not geojson_mask.endswith('.geojson'):
        return False, 'Mask file is not a geoJSON'

    # Check geoJSON is valid
    geojson_df = gpd.read_file(geojson_mask)
    if not geojson_df.is_valid():
        return False, 'GeoJSON file is not valid'

    # TODO check geoJSON bounds with MBTiles

    return True