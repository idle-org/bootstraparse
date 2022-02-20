import bootstraparse.modules.template_mngr as template_mngr
import pytest


@pytest.mark.xfail(reason="Not implemented yet")
def test_get_template_path():
    assert template_mngr.get_template_path() is not None