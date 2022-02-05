# Testing the preparser module
import pytest

from bootstraparse.modules import preparser
from bootstraparse.modules import environment

env = environment.Environment()


@pytest.mark.parametrize("path", ["example_userfiles/index.bpr", "example_userfiles/pages/page1.bpr"])
def test_preparser_init(path):
    """
    Test the preparser module
    """
    pp = preparser.PreParser(path, env)
    assert pp.path == path
    pp.make_import_list()
    pp.open()
    pp.close()
    pp.export_with_imports()
    # pp.export_without_imports()
    assert type(pp.__str__()) == str
    assert type(pp.__repr__()) == str