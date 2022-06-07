# Dedicated module for defining and interpreting errors as well as generating error messages
# You're probably here for log_message or log_exception.
#   They take: message, level=("ERROR, "INFO", "WARNING", "DEBUG", "CRITICAL")
# There's also a dict_check(dic, *args) that returns true if all args are keys in the dict.
# Usage:
#   from bootstraparse.modules.error_mngr import log_message, log_exception
#   log_message("This is a message", level="INFO") level=("ERROR, "INFO", "WARNING", "DEBUG", "CRITICAL")
#   log_exception(Exception("This is an exception"), level="ERROR")
#   dict_check({"a": 1, "b": 2}, "a", "b") # returns [True, True]

import logging
import traceback
from bootstraparse.modules.tools import __GLk  # __GFi, __GFu, __GL


# Define the error codes
_ERRORS = ["ParsingError", "MismatchedContainerError"]
__all__ = _ERRORS+[]


def init_logging(filename=None, loglevel="ERROR", filemode='w', handler=None):
    """
    Initializes logging
    :param filename: The name of the log file
    :param loglevel: The level of logging
    :type loglevel: str
    :param filemode: The mode of the log file
    :param handler: The handler to use
    :return: None
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
        logging.basicConfig(filename=filename, filemode=filemode, level=logging.__getattribute__(loglevel))  # noqa
    else:
        logging.basicConfig(level=logging.__getattribute__(loglevel), handlers=handler)  # noqa


def log_message(message, level="ERROR"):
    """
    Logs a message
    :param message: The message to log
    :param level: The level of the message
    :type level: str
    :return: None
    """
    level = level.lower()
    logging.__getattribute__(level)(' ' + message)
    if level in ["critical"]:
        # logging.__getattribute__(level)(traceback.format_exc())
        # logging.__getattribute__(level)(__GLk())
        print("An unrecoverable error occurred, please check the log file for more information.")


def log_exception(exception, level="ERROR"):
    """
    Logs an exception
    :param exception: The exception to log
    :param level: The level of the exception
    :type level: str
    :return: None
    """
    level = level.lower()
    logging.__getattribute__(level)(traceback.format_exc())
    logging.__getattribute__(level)(__GLk())
    for line in exception.__str__()[0:-1].split('\\n'):
        logging.__getattribute__(level)(' ' + line)
    if level in ["critical", "error"]:
        print("An unrecoverable error occurred, please check the log file for more information.")
        raise exception  # FUTURE: drop the last stack

    if exception.__class__.__name__ == "ParsingError":
        logging.error(exception.__str__())
        logging.debug("A custom RichException has been raised")
        return


def dict_check(dic, *args):
    """
    Helper function to test existence within a dictionary.
    :param dic: The dictionary of dictionaries to check
    :param args: Any number of keys to check the dictionaries for
    :return: A table of Booleans for every key checked.
    """
    output = [False for _ in args]
    for i in range(len(args)):
        if args[i] in dic:
            output[i] = True
            dic = dic[args[i]]
        else:
            break
    return output


def str_dict_check(dic, *args):
    """
    Helper function to test existence within a dictionary and return a string of the values.
    'arg[0]' : True or False

    """
    out = dict_check(dic, *args)
    return "\n".join([f"{args[i]}: {out[i]}" for i in range(len(out))])


class BootstraparseError(Exception):
    pass


class ParsingError(Exception):
    """
    Exception class for parsing errors
    :param message: The message to display
    :type message: str
    :param line: The line number of the error
    :param column: The column number of the error
    :param file: The name of the file
    :return: None
    """

    def __init__(self, message=None, line=None, column=None, file=None):
        """
        Initializes the ParsingError class with the filename and a line and column number
        based on the current position in the file (if available)
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
        :return: The string representation of the ParsingError
        """
        if self.line is not None and self.column is not None and self.file is not None:
            return "[{}] Line {}:{} {}".format(self.file, self.line, self.column, self.args[0])
        else:
            return str(self.message)


class MismatchedContainerError(BootstraparseError):
    """
    The token is not final and cannot be contained. Indicative of a mismatched token.
    """
    def __init__(self, token):  # FUTURE : Add file name to error
        self.token = token
        if token:
            self.line = token.line_number
            self.label = token.label
        else:
            self.line = None
            self.label = None
        super().__init__(f"Could not process {self.label} at line {self.line}.")


class LonelyOptionalError(BootstraparseError):
    """
    Optional token could not be matched with last element in pile (not a container).
    """
    def __init__(self, token, last_in_pile):
        self.token = token
        if token:
            self.line = token.line_number
            self.label = token.label
        else:
            self.line = None
            self.label = None
        if last_in_pile:
            super().__init__(f"Could not match token {token} at line {self.line} with "
                             f"last element in pile {last_in_pile} at line {last_in_pile.line_number} (not a container).")
        else:
            super().__init__(f"Could not match token {token} at line {self.line} "
                             f"as there was nothing in the pile.")
