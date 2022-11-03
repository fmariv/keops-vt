from argparse import ArgumentParser

from mvt_reader import MVTReader


class MVTClipper:
    
    def __init__(self, tiles: str, mask_file: str):
        self.tiles = tiles
        self.mask_file = mask_file


def get_arguments():
    """
    Get and parse the arguments given by the user
    :return: Parsed arguments
    """
    parser = ArgumentParser(description="Clip the vector tiles inside a MBTiles by a mask")
    parser.add_argument('mbtiles',
                        help="MBTiles path",
                        nargs='?',
                        default='no',
                        type=str
                        ) 
    parser.add_argument('mask',
                        help="Mask file path",
                        nargs='?',
                        default='no',
                        type=str
                        )            

    arguments = parser.parse_args()
    return vars(arguments)


if __name__ == '__main__':
    args = get_arguments()
    mvt_reader = MVTReader(args['mbtiles'])
    tiles = mvt_reader.get_decoded_tiles()
    mvt_clipper = MVTClipper(tiles, args['mask'])