import bootstraparse.modules.pathresolver as pathr
import os
import re

pathlike_regexp = r'^([A-z]\:\\|/).+[/\\]src[/\\]bootstraparse[/\\]?$'
test_path = '/a/b/c/test'
test_path_win = test_path.replace('/', '\\')


def test_pathresolver():
    path = pathr.pathresolver(test_path)
    assert path() == os.path.normpath(test_path)
    assert path().replace('/', '\\') == test_path_win
    assert path().replace('\\', '/') == test_path


def test_boostrapath():
    assert re.match(pathlike_regexp, pathr.boostrapath().giveabsolute()) is not None


def test_bpath():
    assert re.match(pathlike_regexp, pathr.bpath()) is not None


if __name__ == "__main__":
    print(test_pathresolver())
