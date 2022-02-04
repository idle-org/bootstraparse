# Test the base parser
from bootstraparse import bparse


def test_to_test():
    assert bparse.to_test() is None
