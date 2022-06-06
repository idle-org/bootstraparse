#!/usr/bin/python3

# Main program, use this to start parsing
import rich

from bootstraparse.modules import sitecreator
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="bootstraparse", description='Parses a folder for all .bpr files and '
                                                                       'magically recreates the same architecture '
                                                                       'with html translated files.')
    parser.add_argument('origin', help='the root folder of all files to parse.')
    parser.add_argument('destination', help="path of the folder where to output all the magic.")
    # parser.add_argument("-v", "verbosity")
    args = parser.parse_args()
    if sitecreator.create_website(args.origin, args.destination) == 0:
        rich.print("Bootstraparse run successful!")

