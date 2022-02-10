# Testing the preparser module
import os
import pathlib
import tempfile

import pytest
# import rich

from bootstraparse.modules import preparser
from bootstraparse.modules import environment

###############################################################################
# Environement variables

env = environment.Environment()
_BASE_PATH_PREPARSER = "../../"
_TEMP_DIRECTORY = tempfile.TemporaryDirectory()


def temp_name(file_name):
    return str(pathlib.Path(_TEMP_DIRECTORY.name, file_name))


_BASE_PATH_GIVEN = "example_userfiles"
_BASE_PATH_ROOT = temp_name(_BASE_PATH_GIVEN)

# ################################################################################
# # Variables to test the preparser module
content_index = """Test content line 1
::< pages/page1.bpr >
Test content line 3
::< pages/page2.bpr >
Test content line 5
::< pages/page1.bpr >
Test content line 7
"""
content_page1 = """Test page1\nTest page1-2\nTest page1-3\n"""
content_page2 = """Test page2\n::< page1.bpr >"""
content_page3 = """Test page3\n::< page3.bpr >"""
content_index_import_list = [(temp_name("pages/page1.bpr"), 1),
                             (temp_name("pages/page2.bpr"), 3),
                             (temp_name("pages/page1.bpr"), 5)]

content_page1_import_list = []
content_page2_import_list = [(temp_name("page1.bpr"), 1)]

final_content_index = """Test content line 1
Test page1
Test page1-2
Test page1-3
Test content line 3
Test page2
Test page1
Test page1-2
Test page1-3
Test content line 5
Test page1
Test page1-2
Test page1-3
Test content line 7
"""
final_content_page1 = """Test page1\nTest page1-2\nTest page1-3\n"""
final_content_page2 = """Test page2\nTest page1\nTest page1-2\nTest page1-3\n"""

website_tree = {
    "index.bpr": content_index,
    "pages/page1.bpr": content_page1,
    "pages/page2.bpr": content_page2
}


@pytest.fixture(autouse=True)
def base_architecture():
    for file_name in website_tree:
        make_new_file(os.path.join(_BASE_PATH_GIVEN, file_name), website_tree[file_name])


def test_base_architecture():
    for e in [temp_name(os.path.join(_BASE_PATH_GIVEN, path)) for path in website_tree.keys()]:
        assert os.path.isfile(e)


def make_new_file(path, content="", mode="w+"):
    """
    Make a new file
    """
    os.makedirs(os.path.dirname(os.path.join(_TEMP_DIRECTORY.name, path)), exist_ok=True)
    with open(os.path.join(_TEMP_DIRECTORY.name, path), mode=mode) as f:
        f.write(content)


def assert_readlines_equals(lines1, lines2):
    for line1, line2 in zip(lines1, lines2):
        assert line1.strip("\n") == line2.strip("\n")


@pytest.mark.parametrize("path, line_found", [
    (temp_name("example_userfiles/index.bpr"), 1),
    (temp_name("example_userfiles/pages/page1.bpr"), 12)
])
def test_preparser_init(path, line_found):
    """
    Test the preparser module initialization and all base functions
    """
    pp = preparser.PreParser(path, env)
    # assert pp.path == path
    # assert pp.name == os.path.basename(path)
    assert pathlib.Path(pp.relative_path_resolver(".")) == pathlib.Path(os.path.dirname(path))
    assert pp.list_of_paths == [path]
    assert pp.global_dict_of_imports == {}
    assert pp.saved_import_list is None
    assert type(pp.__str__()) == str
    assert type(pp.__repr__()) == str


def test_readlines():
    """
    Test the open and close functions
    """
    open_close_file = temp_name("test_open_close.bpr")
    make_new_file(open_close_file, "Test\nline")
    pp = preparser.PreParser(open_close_file, env)
    assert_readlines_equals(pp.readlines(), ["Test", "line"])


@pytest.mark.parametrize("filename, content, expected", [
    ("index.bpr", content_index, content_index_import_list),
    ("page1.bpr", content_page1, content_page1_import_list),
    ("page2.bpr", content_page2, content_page2_import_list),
])
def test_parse_import_list(filename, content, expected, capsys):
    """
    Test the parse_import_list function
    """
    test_file = temp_name(filename)
    make_new_file(test_file, content)

    pp = preparser.PreParser(test_file, env)
    assert pp.parse_import_list() == expected
    assert pp.saved_import_list == expected
    assert pp.parse_import_list() == expected


def test_parse_equals():
    """
    Test the parse_equals function
    """
    test_file = temp_name("test_parse_equals.bpr")
    make_new_file(test_file, "Test line 1\n::< test_parse_equals.bpr >\nTest line 3")
    test_file_2 = temp_name("test_parse_equals_2.bpr")
    make_new_file(test_file_2, "Test line 1\n::< file.bpr >\nTest line 3")

    pp = preparser.PreParser(test_file, env)
    pp2 = preparser.PreParser(test_file, env)
    pp3 = preparser.PreParser(test_file_2, env)
    pp3.parse_import_list()
    pp3.name = pp.name
    pp3.path = pp.path
    pp3.base_path = pp.base_path

    assert pp == pp2
    assert not (pp != pp2)
    assert pp != pp3
    pp3.name = "test_parse_equals_2.bpr"
    assert pp != pp3


@pytest.mark.parametrize("filename, content", [
    ("index.bpr", content_index),
    ("pages/page1.bpr", content_page1),
    ("pages/page2.bpr", content_page2),
])
def test_make_import_list(filename, content, capsys):
    """
    Test the make_import_list function
    """
    testfile = temp_name(os.path.join(_BASE_PATH_GIVEN, filename))

    assert os.path.exists(testfile)
    pp = preparser.PreParser(testfile, env)
    pp.make_import_list()
    # Creating a real file to compare with is not a good idea on the long run
    # Will compare the dicts instead
    assert pp.global_dict_of_imports.keys() == set([f for f, _ in pp.saved_import_list])


@pytest.mark.parametrize("filename, content", [
    ("index.bpr", final_content_index),
    ("pages/page1.bpr", final_content_page1),
    ("pages/page2.bpr", final_content_page2),
])
def test_preparser_content(filename, content):
    """
    Test the preparser content
    """
    testfile = temp_name(os.path.join(_BASE_PATH_GIVEN, filename))
    assert os.path.exists(testfile)
    pp = preparser.PreParser(testfile, env)
    pp.make_import_list()

    assert pp.export_with_imports().read() == content  # nothing is implementes yet
    # todo: test import in sub-folders


# @pytest.mark.skip("Not implemented")
def test_errors():
    with pytest.raises(FileNotFoundError):
        pp = preparser.PreParser("not_existing_file.bprr", env)
        pp.readlines()

    with pytest.raises(ImportError):
        nofile = temp_name("real_file.bpr")
        make_new_file(nofile, "::< not_existing_file.bpr >")
        pp = preparser.PreParser(nofile, env)
        pp.make_import_list()

    with pytest.raises(RecursionError):
        path = temp_name("test_recursion_error.bpr")
        make_new_file(path, "::< test_recursion_error.bpr >")
        pp = preparser.PreParser(path, env)
        pp.make_import_list()


def test_rich_tree():
    """
    Test the rich_tree function
    """
    test_file = temp_name("test_rich_tree.bpr")
    test_file_2 = temp_name("test_rich_tree_2.bpr")
    make_new_file(test_file, "Test line 1\n::< test_rich_tree_2.bpr >\nTest line 3")
    make_new_file(test_file_2, "Test line 1\nTest line 3")
    pp = preparser.PreParser(test_file, env)
    pp.make_import_list()
    pp.rich_tree()
    pp.rich_tree(force=False)
