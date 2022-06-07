import pytest

from bootstraparse.modules import syntax, error_mngr, tools, context_mngr
from bootstraparse.modules.tools import __GL, __module_path, find_variables_in_file

__XF = pytest.mark.xfail

_list_original_strings = [
    "string",
]


def test_to_original():
    """Test the .to_original() method of SemanticTypes."""
    token = syntax.SemanticType(["test"])
    assert token.to_original() == 'test'
