import os
import tempfile

import pytest
import rich

import bootstraparse.modules.sitecrawler as sitecrawler
from bootstraparse.modules import environment, config, pathresolver, export

_TEMP_DIRECTORY = tempfile.TemporaryDirectory()
_BASE = os.path.join(_TEMP_DIRECTORY.name, "base")
_DEST = os.path.join(_TEMP_DIRECTORY.name, "dest")
files = [
    ("base/test1.bpr", ""),
    ("base/test2.bpr", ""),
    ("base/test3.bpr", ""),
    ("base/_noimport.bpr", ""),
    ("base/subtests/test4.bpr", ""),
    ("base/subtests/test5.bpr", ""),
    ("base/config/test6.yml", ""),
    ("base/config/test7.yml", ""),
    ("base/templates/test8.yml", ""),
]


def make_new_file(path, content="", mode="w+"):
    """
    Make a new file
    """
    name = os.path.join(_TEMP_DIRECTORY.name, path)
    os.makedirs(os.path.dirname(name), exist_ok=True)
    # print(f"Creating : {name}")
    # print(f"Content  : {content}")
    # print(f"Location : {os.path.dirname(name)}")
    # print()
    with open(name, mode=mode) as f:
        f.write(content)
    return name


@pytest.fixture(scope="module")
def list_files():
    """
    List all files in the test directory
    """
    return [make_new_file(file, content) for file, content in files]


@pytest.fixture(scope="module")
def env():
    env = environment.Environment()
    env.config = config.ConfigLoader(pathresolver.b_path("configs"))
    if os.path.exists(os.path.join(_BASE, "configs")):
        env.config.add_folder(os.path.join(_BASE, "configs"))

    env.template = config.ConfigLoader(pathresolver.b_path("templates"))
    if os.path.exists(os.path.join(_BASE, "templates")):
        env.template.add_folder(os.path.join(_BASE, "templates"))

    env.export_mngr = export.ExportManager(env.config, env.template)
    env.origin = _BASE
    env.destination = _DEST
    return env


def test_bad_site_creator(env):
    with pytest.raises(FileNotFoundError):
        sitecrawler.SiteCrawler("NONEXISTENT", _DEST, env)


def test_sitecrawler(list_files, env):
    """
    Test the sitecrawler.SiteCrawler class
    """

    crw = sitecrawler.SiteCrawler(_BASE, _DEST, env)
    rich.inspect(crw)
    crw.set_all_preparsers()
    for pre, dest in crw:
        assert os.path.exists(dest)
        assert os.path.isfile(dest)

    crw.force_rewrite = False
    with pytest.raises(FileExistsError):
        crw.set_all_preparsers()
    crw.force_rewrite = True
    crw.set_all_preparsers()


@pytest.mark.skip(reason="Not implemented")
def test_result_crawler(list_files, env):
    """
    Test the sitecrawler.ResultCrawler class
    """
    pass
