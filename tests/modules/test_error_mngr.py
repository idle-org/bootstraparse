# Testing the error manager
import logging
from collections import namedtuple
from importlib import reload
from unittest import TestCase
import pytest
import bootstraparse.modules.error_mngr as error_mngr
from bootstraparse.modules.error_mngr import ParsingError, MismatchedContainerError

all_logging_tests = [(i, j, k) for i in [None, "test.log"]
                     for j in ["DEBUG", "INFO",  "WARNING", "ERROR", "CRITICAL", "NOPE_PARAM"]
                     for k in ["rich", None]]
all_non_blocking_exception_tests = [
    (ParsingError("test error", 10, 10, "testfile.bpr")),
    (ParsingError()),
    (MismatchedContainerError(namedtuple("Test", ["label", "line_number"])("test", 10),)),
]
all_blocking_exception_tests = [

]


class TestLogging(TestCase):
    def test_init_logging(self):
        for filename, level, handler in all_logging_tests:
            with self.assertLogs() as captured:
                error_mngr.init_logging(filename=filename, loglevel=level, handler=handler)
                logging.critical("Logging initialized", exc_info=True)
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].levelname, "CRITICAL")
            self.assertEqual(captured.records[0].msg, "Logging initialized")
            re_import_log()

    def test_log_exception(self):
        with self.assertLogs() as captured:
            with pytest.raises(SystemExit):
                error_mngr.log_exception(Exception(''), level="CRITICAL")
        self.assertGreaterEqual(len(captured.records), 3)

    def test_log_exception_with_message(self):
        for exception in all_non_blocking_exception_tests:
            with self.assertLogs() as captured:
                error_mngr.log_exception(exception, level="Warning")
            self.assertGreaterEqual(len(captured.records), 1)

        for exception in all_blocking_exception_tests:
            with self.assertLogs() as captured:
                with pytest.raises(SystemExit):
                    error_mngr.log_exception(exception, level="CRITICAL")
            self.assertGreaterEqual(len(captured.records), 4)

    def test_log_message(self):
        with self.assertLogs() as captured:
            error_mngr.log_message("test message", level="INFO")
        self.assertEqual(len(captured.records), 1)
        self.assertEqual("INFO", captured.records[0].levelname)
        self.assertEqual(" test message", captured.records[0].msg)

    def test_log_message_critical(self):
        with self.assertLogs() as captured:
            error_mngr.log_message("test message", level="CRITICAL")
        self.assertGreaterEqual(len(captured.records), 1)
        self.assertEqual("CRITICAL", captured.records[0].levelname)
        self.assertEqual(" test message", captured.records[0].msg)


def test_exception__str__():
    """
    Test the __str__ method of the exception, to make sure it is working
    Doesn't test the actual str returned, just that it is a string
    """
    for exception in all_non_blocking_exception_tests:
        text = exception.__str__()
        assert(type(text) == str)


def re_import_log():
    logging.shutdown()
    reload(logging)


def test_dict_check():
    """
    Test the dict_check function
    """
    assert(error_mngr.dict_check({"test": "test"}, "test") == [True])
    assert(error_mngr.dict_check({"test": "test"}, "test2") == [False])
    assert(error_mngr.dict_check({"test": {"test3": "test5"}}, "test", "test3") == [True, True])
    assert(error_mngr.dict_check({"test": {"test3": "test5"}}, "test4", "test4") == [False, False])
    assert(error_mngr.dict_check({"test": {"test3": "test5"}}, "test", "test34") == [True, False])


# @pytest.mark.xfail(strict=True, reason="This test is not implemented yet")
def test_dict_check_2():
    assert(error_mngr.dict_check({"test": "test"}, "test", "test2") == [True, False])
    assert(error_mngr.dict_check({"test": "test"}, "test", "test2", "test3") == [True, False, False])


def test_dict_str():
    assert error_mngr.str_dict_check({"test": "test"}, "test") == "test: True"
    assert error_mngr.str_dict_check({"test": "test"}, "test2") == "test2: False"
    assert error_mngr.str_dict_check({"test": {"test3": "test5"}}, "test", "test3") == "test: True\ntest3: True"


def test_weird_exception_cases():
    with pytest.raises(error_mngr.MismatchedContainerError):
        raise(error_mngr.MismatchedContainerError(None))

    with pytest.raises(error_mngr.LonelyOptionalError):
        raise(error_mngr.LonelyOptionalError(None, None))

    from typing import NamedTuple
    tk = NamedTuple("falsetoken", [("line_number", int), ("label", str)])(1, "test")
    with pytest.raises(error_mngr.LonelyOptionalError):
        raise(error_mngr.LonelyOptionalError(tk, None))


if __name__ == '__main__':
    TestLogging().test_init_logging()
