import bootstraparse.modules.context_mngr as context_mngr
import pytest


@pytest.mark.xfail(reason="Not implemented yet")
def test_context_mngr_init():
    context_mngr.ContextManager()
