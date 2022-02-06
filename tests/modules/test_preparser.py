# Testing the preparser module

import pytest
import io

from bootstraparse.modules import preparser
from bootstraparse.modules import environment

env = environment.Environment()


@pytest.mark.parametrize("path", ["example_userfiles/index.bpr", "example_userfiles/pages/page1.bpr"])
def test_preparser_init(path):
    """
    Test the preparser module initialization and all base functions
    """
    pp = preparser.PreParser(path, env)
    assert pp.path == path
    pp.make_import_list()
    pp.open()
    pp.close()
    pp.export_with_imports()
    pp.readlines()
    # pp.export_without_imports()

    assert type(pp.__str__()) == str
    assert type(pp.__repr__()) == str


################################################################################
# False functions to simulate a full import tree
def false_file_open(text):
    def _file_open():
        return io.StringIO(text)
    return _file_open


def false_import_list(table):
    def _import_list():
        return table
    return _import_list


def assert_readlines_equals(lines1, lines2):
    for line1, line2 in zip(lines1, lines2):
        assert line1.strip("\n") == line2.strip("\n")


def make_false_PreParser(path, list_imports, content):
    pp = preparser.PreParser(path, env)
    pp.open = false_file_open(content)
    pp.parse_import_list = false_import_list(list_imports)
    pp.make_import_list()
    return pp


################################################################################
# Variables to test the preparser module
content_index = """Test content
::< exemple_userfiles/pages/page1.bpr >
Test content
::< exemple_userfiles/pages/page2.bpr >
Test content
::< exemple_userfiles/pages/page1.bpr >
Test content"""
content_page1 = """Test page1"""
content_page2 = """Test page2"""
content_import_list = ["exemple_userfiles/pages/page1.bpr",
                       "exemple_userfiles/pages/page2.bpr",
                       "exemple_userfiles/pages/page1.bpr"]

final_content = """Test content
Test page1
Test content
Test page2
Test content
Test page1
Test content"""


@pytest.fixture(scope="module")
def p_index():
    return make_false_PreParser("example_userfiles/index.bpr", content_import_list, content_index)


################################################################################
# Test the preparser module
@pytest.mark.xfail(reason="Not implemented", raises=NotImplementedError)
def test_import_list():
    p_index = preparser.PreParser("example_userfiles/index.bpr", env)
    p_index.open = false_file_open(content_index)
    try:
        assert p_index.make_import_list() == content_import_list
    except AssertionError:
        p_index.parse_import_list = false_import_list(content_import_list)
        raise NotImplementedError("Import list is not correct")


@pytest.mark.xfail(reason="Not implemented", raises=NotImplementedError)
def test_preparser_content(p_index):
    p_index.make_import_list()
    assert_readlines_equals(p_index.readlines(), content_index.split("\n"))

    # Test the recursion error
    with pytest.raises(RecursionError):
        p_index.list_of_paths = ["exemple_userfiles/pages/page1.bpr"]
        p_index.make_import_list()

    p_page1 = make_false_PreParser("exemple_userfiles/pages/page1.bpr", content_import_list, content_page1)
    assert p_page1.open().readlines() == ["Test page1"]

    p_page2 = make_false_PreParser("exemple_userfiles/pages/page2.bpr", content_import_list, content_page2)
    assert p_page2.open().readlines() == ["Test page2"]

    try:
        assert_readlines_equals(p_index.export_with_imports(), final_content.split("\n"))
    except AssertionError:
        raise NotImplementedError("Export with imports is not correct")
