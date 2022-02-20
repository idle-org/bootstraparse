import bootstraparse.modules.export as export
import pytest


@pytest.mark.xfail(reason="Not implemented")
def test_export():
    assert export.export() == "export"
