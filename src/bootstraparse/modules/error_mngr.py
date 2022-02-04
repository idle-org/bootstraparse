# Dedicated module for defining and interpreting errors as well as generating error messages

import logging
import traceback
import sys

# Define the error codes
__all__ = ["ParsingError"]


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
    if level in ["critical"]:
        print("An unrecoverable error occurred, please check the log file for more information.")
        sys.exit()
        # raise exception  # Re-raises the exception

    if exception.__class__.__name__ == "ParsingError":
        logging.error(exception.__str__())
        logging.debug("A custom RichException has been raised")
        return


class ParsingError(Exception):
    """
    Exception class for parsing errors
    """

    def __init__(self, message=None, line=None, column=None, file=None):
        """
        Initializes the ParsingError class with the filename and a line and column number based on the current position in the file (if available)
        """
        super().__init__(message)
        self.line = line
        self.column = column
        self.file = file
        self.message = message
        if self.message is None:
            self.message = "A {} error occurred".format(self.__class__.__name__)

    def __str__(self):
        """
        Returns a string representation of the ParsingError
        """
        if self.line is not None and self.column is not None and self.file is not None:
            return "[{}] Line {}:{} {}".format(self.file, self.line, self.column, self.args[0])
        else:
            return str(self.message)
