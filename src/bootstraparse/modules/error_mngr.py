# Dedicated module for defining and interpreting errors as well as generating error messages

import logging
import traceback
import sys


def initlogging(filename=None, loglevel="ERROR", filemode='w', handlers=None):
    """
    Initializes logging
    """
    loglevel = loglevel.upper()
    if loglevel not in ["ERROR", "INFO", "WARNING", "DEBUG", "CRITICAL"]:
        print("Incorrect logging", loglevel + ". Defaulting to ERROR.")
        loglevel = "ERROR"
    if handlers == "rich":
        from rich.logging import RichHandler
        handlers = [RichHandler()]
    else:
        handlers = []

    if filename is not None:
        logging.basicConfig(filename=filename, filemode=filemode, level=logging.__getattribute__(loglevel))
    else:
        logging.basicConfig(level=logging.__getattribute__(loglevel), handlers=handlers)


def log_exception(exception, level="ERROR"):
    """
    Logs an exception
    """
    level = level.lower()
    logging.__getattribute__(level)(traceback.format_exc())
    if level == "error":
        print("An unrecoverable error occurred, please check the log file for more information.")
        sys.exit()
        # raise exception

    if exception.__class__.__name__ == "RichException":
        logging.error(exception.__str__())
        logging.debug("A custom RichException has been raised")
        return

def raiseE():
    """
    Raises an exception
    """
    raise Exception("The parser encountered an error")


if __name__ == "__main__":
    initlogging(handlers="rich", filename="test.log")
    logging.error("This is a debug message")
    try:
        raiseE()
    except Exception as e:
        log_exception(e)
