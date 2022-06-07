#!/usr/bin/python3

# Main program, use this to start parsing

from bootstraparse.modules import sitecreator
import argparse
import sys


def parse(_args):
    parser = argparse.ArgumentParser(
        prog="bootstraparse",
        description='Parses a folder for all .bpr files and magically recreates the same architecture '
                    'with html translated files.'
    )
    parser.add_argument('origin', help='the root folder of all files to parse.')
    parser.add_argument('destination', help="path of the folder where to output all the magic.")
    # parser.add_argument("-v", "verbosity")
    return parser.parse_args(_args)


if __name__ == "__main__":  # pragma: no cover
    args = parse(sys.argv[1:])
    if sitecreator.create_website(args.origin, args.destination) == 0:
        print("Bootstraparse run successful!")
