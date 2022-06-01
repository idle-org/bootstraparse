# Testing the preparser module
import os
import pathlib
import tempfile
from io import StringIO
from itertools import zip_longest

import pytest
import rich

from bootstraparse.modules import preparser, config, pathresolver
from bootstraparse.modules import environment
from bootstraparse.modules import export

###############################################################################
# Environment variables

env = environment.Environment()
env.export_mngr = export.ExportManager('', '')
env.config = config.ConfigLoader(pathresolver.b_path("../../example_userfiles/config/"))
env.export_mngr = export.ExportManager('', '')
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
content_page3 = """Test page3\n::< subpages/page3.bpr > < subpages/spage4.bpr > <subpages/spage5.bpr > <subpages/spage6.bpr > < page4.bpr >"""
content_page4 = """Test page4\n::< page5.bpr > < page6.bpr > < ../index.bpr >"""
content_page5 = """Test page5\n::"""
content_page6 = """Test page6\n::"""
content_superimports = """Test superimports\n::< pages/page3.bpr > < pages/subpages/page3.bpr >"""
content_sub_page3 = """Test sub page3\n::< spage4.bpr >"""
content_sub_page4 = """Test sub page4\n::< spage5.bpr > < spage6.bpr > < ../../index.bpr >"""
content_sub_page5 = """Test sub page5"""
content_sub_page6 = """Test sub page6"""

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
final_content_superimports = """Test superimports\nTest page3\nTest sub page3\nTest sub page4
Test sub page5Test sub page6Test content line 1\nTest page1\nTest page1-2\nTest page1-3
Test content line 3\nTest page2\nTest page1\nTest page1-2\nTest page1-3\nTest content line 5
Test page1\nTest page1-2\nTest page1-3\nTest content line 7\nTest sub page4
Test sub page5Test sub page6Test content line 1\nTest page1\nTest page1-2
Test page1-3\nTest content line 3\nTest page2\nTest page1\nTest page1-2
Test page1-3\nTest content line 5\nTest page1\nTest page1-2\nTest page1-3
Test content line 7\nTest sub page5Test sub page6Test page4\nTest page5
::Test page6\n::Test content line 1\nTest page1\nTest page1-2\nTest page1-3
Test content line 3\nTest page2\nTest page1\nTest page1-2\nTest page1-3
Test content line 5\nTest page1\nTest page1-2\nTest page1-3\nTest content line 7
Test sub page3\nTest sub page4\nTest sub page5Test sub page6Test content line 1
Test page1\nTest page1-2\nTest page1-3\nTest content line 3\nTest page2\nTest page1
Test page1-2\nTest page1-3\nTest content line 5\nTest page1\nTest page1-2\nTest page1-3
Test content line 7\n"""

final_content_page1 = """Test page1\nTest page1-2\nTest page1-3\n"""
final_content_page2 = """Test page2\nTest page1\nTest page1-2\nTest page1-3\n"""
website_tree = {
    "index.bpr": content_index,
    "superimports.bpr": content_superimports,
    "pages/page1.bpr": content_page1,
    "pages/page2.bpr": content_page2,
    "pages/page3.bpr": content_page3,
    "pages/page4.bpr": content_page4,
    "pages/page5.bpr": content_page5,
    "pages/page6.bpr": content_page6,
    "pages/subpages/page3.bpr": content_sub_page3,
    "pages/subpages/spage4.bpr": content_sub_page4,
    "pages/subpages/spage5.bpr": content_sub_page5,
    "pages/subpages/spage6.bpr": content_sub_page6,
}

get_from_config = '''@{do_not_remove_p} {whatever_picture} ["whateverpicture", i=42]
@{do_not_remove_p}{class="shortcut", type=2, name="shortcut"}[type=33, name="shortcut"]{{classinsert}}
@[do_not_remove_s]{class="picture", type=2, name="picture"}[type=33, name="picture"]{{hello}}
@[do_not_remove_f]{class="picture", type=2, name="picture"}[12,1222, a=33, b="picture"]{{hello}}
@{do_not_remove_f}[a=33, b="picture", 42, 4242.477]{{hello}}
'''
final_from_config = """<img src="This is a test" whatever_picture/>
<img src="This is a test" class="shortcut", type=2, name="shortcut" class="classinsert"/>
This is a test
This is a test 12 1222 33 picture
<img src="This is a test 42 4242.477 33 picture" class="hello"/>
"""


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
    for line1, line2 in zip_longest(lines1, lines2):
        assert line1.strip("\n") == line2.strip("\n")
    return True


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

    assert pp.export_with_imports().read() == content


def test_subfolder_parsing():
    """
    Test the preparser content
    """
    testfile = temp_name(os.path.join(_BASE_PATH_GIVEN, "superimports.bpr"))
    assert os.path.exists(testfile)
    pp = preparser.PreParser(testfile, env)
    pp.make_import_list()
    rich.print(pp.rich_tree())
    assert pp.export_with_imports().read() == final_content_superimports


def test_do_imports():
    """
    Test the full export function
    """
    testfile = temp_name(os.path.join(_BASE_PATH_GIVEN, "index.bpr"))
    assert os.path.exists(testfile)
    pp = preparser.PreParser(testfile, env)
    pp.do_imports()
    f = pp.do_replacements()
    assert f.read() == final_content_index


def test_get_all_lines():
    """
    Test the line reader
    """
    testfile = temp_name(os.path.join(_BASE_PATH_GIVEN, "index.bpr"))
    assert os.path.exists(testfile)
    pp = preparser.PreParser(testfile, env)
    assert_readlines_equals(pp.get_all_lines(), content_index.split("\n")[:-1])

    # To test we are getting the right file
    pp.current_origin_for_read = StringIO("12")
    assert pp.get_all_lines() == ['12']

    # To test we are getting the right file
    pp.do_replacements()
    pp.current_origin_for_read = StringIO("123")
    assert pp.get_all_lines() == ["123"]
    assert pp.readlines() != pp.get_all_lines()


def test_new_temporary_files():
    """
    Test the reset of the files
    """
    testfile = temp_name(os.path.join(_BASE_PATH_GIVEN, "index.bpr"))
    assert os.path.exists(testfile)
    pp = preparser.PreParser(testfile, env)
    pp.do_imports()
    pp.do_replacements()
    pp.new_temporary_files()
    assert_readlines_equals(pp.readlines(), content_index.split("\n")[:-1])
    assert_readlines_equals(pp.get_all_lines(), final_content_index.split("\n")[:-1])
    assert pp.file_with_all_imports.read() == ""
    assert pp.file_with_all_replacements.read() == ""
    pp.do_imports()
    pp.do_replacements()
    assert_readlines_equals(pp.get_all_lines(), final_content_index.split("\n")[:-1])


def test_errors():
    with pytest.raises(FileNotFoundError):
        pp = preparser.PreParser("not_existing_file.bprr", env)
        pp.readlines()

    with pytest.raises(ImportError):  # Not ImportError
        nofile = temp_name("real_file.bpr")
        make_new_file(nofile, "::< not_existing_file.bpr >")
        pp = preparser.PreParser(nofile, env)
        pp.make_import_list()

    with pytest.raises(RecursionError):  # Not RecursionError
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


def test_get_shortcut_from_config():
    from_config = temp_name("get_from_config.bpr")
    make_new_file(from_config, get_from_config)
    assert os.path.exists(from_config)

    pp = preparser.PreParser(from_config, env)
    pp.do_imports()
    pp.parse_shortcuts_and_images()
    assert pp.get_image_from_config("do_not_remove_p", "") == '''<img src="This is a test"/>'''
    assert pp.get_alias_from_config("do_not_remove_s", None) == "This is a test"
    assert assert_readlines_equals(pp.do_replacements().readlines(), final_from_config.split("\n")[:-1])


def test_replace():
    replace_file = temp_name("test_preparse.bpr")
    make_new_file(replace_file, get_from_config)
    pp = preparser.PreParser(replace_file, env)

    pp.make_import_list()
    pp.export_with_imports()
    image_f = pp.parse_shortcuts_and_images()
    assert assert_readlines_equals(image_f.readlines(), final_from_config.split("\n")[:-1])


def test_early_tree(base_architecture):
    tree_file = temp_name(os.path.join(_BASE_PATH_GIVEN, "index.bpr"))
    assert os.path.exists(tree_file)
    pp = preparser.PreParser(tree_file, env)

    rich.print(pp.rich_tree())


def test_get_errors():
    from_config = temp_name("test_get_errors.bpr")
    pp = preparser.PreParser(from_config, env)
    assert pp.get_element_from_config("aliases", "shortcuts", "do_not_remove_s") == "This is a test"
    assert pp.get_element_from_config("aliases", "images", "do_not_remove_p") == 'This is a test'
    with pytest.raises(KeyError):
        pp.get_element_from_config("aliases", "not_existing", "do_not_remove_s")
    with pytest.raises(KeyError):
        pp.get_element_from_config("images", "not_existing", "do_not_remove_p")


def test_make_replacement_errors():
    from_config = temp_name("test_get_errors.bpr")
    pp = preparser.PreParser(from_config, env)
    assert pp.make_replacements("This is a test") == "This is a test"
    assert pp.make_replacements("This is a test", "not_existing") == "This is a test"
    assert pp.make_replacements("This is a test {}", "shortcuts") == "This is a test shortcuts"
    assert pp.make_replacements("This is a test {}", "images") == "This is a test images"
    assert pp.make_replacements("This is a test {} {} {image} {b}", 1, 2, image="images", b="b") == "This is a test 1 2 images b"
    assert pp.make_replacements("This is a test {} {} {image} {b}", karm=3) == "This is a test {} {} {image} {b}"
