import bootstraparse.modules.pathresolver as path_r
import os
import re

path_like_regexp = r'^([A-z]\:\\|/).+[/\\]src[/\\]bootstraparse[/\\]?$'
test_path = '/a/b/c/test'
test_path_win = test_path.replace('/', '\\')


def test_PathResolver():
    path = path_r.PathResolver(test_path)
    assert path() == os.path.normpath(test_path)
    assert path().replace('/', '\\') == test_path_win
    assert path().replace('\\', '/') == test_path


def test_BoostraPath():
    assert re.match(path_like_regexp, path_r.BoostraPath().give_absolute()) is not None


def test_b_path():
    assert re.match(path_like_regexp, path_r.b_path()) is not None
