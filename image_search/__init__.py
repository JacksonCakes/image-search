import warnings
warnings.simplefilter("ignore", UserWarning)

from image_search.options import parse_args
from image_search.app import main

def entry_point():
    args = parse_args()
    main(args)