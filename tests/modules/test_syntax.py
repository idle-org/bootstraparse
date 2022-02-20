import bootstraparse.modules.syntax as syntax
import pytest


@pytest.mark.xfail(reason="Not implemented")
def test_syntax_check():
    assert syntax.syntax_check() == True
