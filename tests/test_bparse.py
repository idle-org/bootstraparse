# Test the base parser

from bootstraparse import __main__


def test_to_test():
    args = __main__.parse(["path1", "path2"])
    assert args.origin == "path1"
    assert args.destination == "path2"
