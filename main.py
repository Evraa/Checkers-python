import constants
from solve import main
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--board_size", required=True)
    parser.add_argument("-g", "--greedy", required=False)
    parser.add_argument("-ag", "--against", required=False)
    parser.add_argument("-l", "--level", required=True)
    parser.add_argument("-v", "--verbose", required=False)
    parser.add_argument("-gfx", "--gfx", required=False)
    parser.add_argument("-p", "--prune", required=True)
    parser.add_argument("-vd", "--verbose_deep", required=False)    
    args = parser.parse_args()
    constants.parse_constants(args)
    