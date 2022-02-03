# Testing the error manager
import logging
from importlib import reload

import pytest

import bootstraparse.modules.error_mngr as error_mngr



@pytest.parametrize("filename, level, handler", [(i, j, k) for i in [None, "test.log"] for j in ["DEBUG", "INFO",
                                                        "WARNING", "ERROR", "CRITICAL"] for k in ["rich", None]])
def test_initlogging(filename, level, handler):
    import logging
    error_mngr.initlogging(filename=None, loglevel="DEBUG",handler=None)
    logging.error("Logging initialized", exc_info=True)
    reimport_log()
    error_mngr.initlogging(filename="testr.log", loglevel="DEBUG",handler=None)
    logging.info("Logging initialized", exc_info=True)


def reimport_log():
    logging.shutdown()
    reload(logging)


if __name__ == "__main__":
    test_initlogging()