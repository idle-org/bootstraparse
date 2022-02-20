import bootstraparse.modules.config as config
import pytest


"""
"""


@pytest.mark.xfail(reason="Not implemented")
def test_config_load():
    assert config.load() is not None
