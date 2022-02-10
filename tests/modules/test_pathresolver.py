import pathlib

import bootstraparse.modules.pathresolver as path_r
import re
import pytest

path_like_regexp = r'^([A-z]\:\\|/).+[/\\]src[/\\]bootstraparse[/\\]?$'
# test_path = '/a/b/c/test'
# test_path_win = test_path.replace('/', '\\')


def test_BoostraPath():
    assert re.match(path_like_regexp, path_r.BoostraPath().give_absolute()) is not None


def test_b_path():
    assert re.match(path_like_regexp, path_r.b_path()) is not None


@pytest.mark.parametrize('init,path,result', [
    ('/a/b/c/', '..', "/a/b"),
    ('/a/b/c/', '../..', "/a"),
    ('/a/b/c/', '../../..', "/"),
    ('/a/b/c/test.py', '.', '/a/b/c/'),
    ('/a/b/c/test.py', './', '/a/b/c/'),
    ('/a/b/c/test.py', './test2.py', '/a/b/c/test2.py'),
    ('/a/b/c/test.py', '../test2.py', '/a/b/test2.py'),
    ('/a/b/c/test.py', '/d/test2.py', '/d/test2.py'),
    ('/a/b/c/test.py', '../d/test2.py', '/a/b/d/test2.py'),
])
def test_path_call(init, path, result):
    assert pathlib.Path(path_r.PathResolver(init)(path)).parts[1:] == pathlib.Path(result).parts[1:]
