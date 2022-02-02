# Dedicated module for defining and interpreting errors as well as generating error messages

import logging
import traceback
import sys


def initlogging(filename=None, loglevel="ERROR", filemode='w', handler=None):
    """
    Initializes logging
    """
    loglevel = loglevel.upper()
    if loglevel not in ["ERROR", "INFO", "WARNING", "DEBUG", "CRITICAL"]:
        print("Incorrect logging", loglevel + ". Defaulting to ERROR.")
        loglevel = "ERROR"
    if handler == "rich":
        from rich.logging import RichHandler
        handler = [RichHandler()]
    else:
        handler = []

    if filename is not None:
        logging.basicConfig(filename=filename, filemode=filemode, level=logging.__getattribute__(loglevel))
    else:
        logging.basicConfig(level=logging.__getattribute__(loglevel), handlers=handler)


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


class ParsingError(Exception):
    """
    Exception class for parsing errors
    """

    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.line = line
        self.column = column

    def __str__(self):
        if self.line is not None and self.column is not None:
            return "Line " + str(self.line) + ":" + str(self.column) + ": " + self.args[0]
        else:
            return self.args[0]
