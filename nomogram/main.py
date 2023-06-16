import sys
import argparse
import pandas as pd
from nomogram import nomogram


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser('Nomogram for logisics regression model', add_help=False)
    parser.add_argument('--weights_path', type=str, default='', help='The table that contain the lr weights and data description characteritics')
    parser.add_argument('--nomo_title', type=str, default='', help='The title of nomogram')
    parser.add_argument('--save_path', type=str, default='./nomogram.png', help='The path of saved nomogram')
    args = parser.parse_args()

    if not args.weights_path:
        print("Plase input the path of the weights saved file")
        sys.exit(0)

    nomogram(path = args.weights_path, result_title=args.nomo_title, savefig=args.save_path)
