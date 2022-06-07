import os
import tempfile

import pytest

from bootstraparse.modules import sitecreator, syntax, context_mngr

_TEMP_DIRECTORY = tempfile.TemporaryDirectory()
_BASE = os.path.join(_TEMP_DIRECTORY.name, "base")
_DEST = os.path.join(_TEMP_DIRECTORY.name, "dest")
files = [
    ("base/test1.bpr", "*Test*", "<em>Test</em>\n"),
    ("base/test2.bpr", ":: <_noimport.bpr>", '<a href="link://dest">linktext</a>\n'),
    ("base/test3.bpr", "#. List", "<ol>\n<li>List</li>\n</ol>"),
    ("base/_noimport.bpr", "[linktext]('link://dest')", None),
    ("base/subtests/test4.bpr", "# Header #", "<h1>Header </h1>\n"),
    ("base/subtests/test5.bpr", "<<div\ntest\ndiv>>", "<div>\n test \n</div>\n"),
    ("base/configs/test6.yml", "test: test", None),
    ("base/configs/test7.yml", "test: test", None),
    ("base/templates/test8.yml", "test: test", None),
]


def make_new_file(path, content="", mode="w+"):
    """
    Make a new file
    """
    name = os.path.join(_TEMP_DIRECTORY.name, path)
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, mode=mode) as f:
        f.write(content)
    return path


@pytest.fixture(scope="module")
def list_files():
    """
    List all files in the test directory
    """
    return [(os.path.join(_DEST, make_new_file(file, content).split("/", 1)[1].replace(".bpr", ".html")), exp)
            for file, content, exp in files]


@pytest.fixture(scope="module")
def env():
    return sitecreator.create_environment(_BASE, _DEST)


def test_create_site(env, list_files):
    sitecreator.create_website(_BASE, _DEST)
    for file, exp in list_files:
        if exp is not None:
            assert os.path.exists(file)
            with open(file, "r") as f:
                assert f.read() == exp


def test_save(list_files, env):
    containers = [
        context_mngr.TextContainer([syntax.TextToken(["Test"])]),
        context_mngr.TextContainer([syntax.TextToken(["Test2"])]),
    ]
    fd = make_new_file(os.path.join(_DEST, "filetest.html"))
    sitecreator.save(containers, os.path.join(_DEST, "filetest.html"), env)
    with open(fd, "r") as f:
        assert f.read() == "TestTest2"
