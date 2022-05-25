# Main parser, gets config files and parses them for the context manager.
# parse_line takes a io and outputs it all as a list of parsed elements
# TODO: decide the parser scope
from io import StringIO

import rich

import bootstraparse.modules.syntax as syntax


def parse_line(io):
    """
    Takes an io string and returns the parsed output.
    :param io: io.StringIO
    :params
    :io: io string input
    :rtype: list
    :return: a list of parsed objects
    """
    output = []
    for line in io.readlines():
        output += syntax.line.parseString(line).asList() + [syntax.Linebreak('')]

    return output


if __name__ == "__main__":
    hello = StringIO(
        """
        *hellooooooooooooooooooooooooooooooooooooooooooooooooo*
        my name is **bernard**
        # hello #
        """
    )
    print(parse_line(hello))
