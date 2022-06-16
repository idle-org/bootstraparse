"""
Dedicated module for defining and interpreting errors as well as generating error messages
You're probably here for log_message or log_exception.
 - They take: message, level=("ERROR, "INFO", "WARNING", "DEBUG", "CRITICAL")
There's also a dict_check(dic, *args) that returns true if all args are keys in the dict.
Usage:
 - from bootstraparse.modules.error_mngr import log_message, log_exception
 - log_message("This is a message", level="INFO") level=("ERROR, "INFO", "WARNING", "DEBUG", "CRITICAL")
 - log_exception(Exception("This is an exception"), level="ERROR")
 - dict_check({"a": 1, "b": 2}, "a", "b") # returns [True, True]
"""

import logging
import traceback
from bootstraparse.modules.tools import __GLk  # __GFi, __GFu, __GL


# Define the error codes
_ERRORS = ["ParsingError", "MismatchedContainerError"]


def init_logging(filename=None, loglevel="ERROR", filemode='w', handler=None):
    """
    Initializes logging
    :param filename: The path for the log file
    :param loglevel: The level of logging: "ERROR", "INFO", "WARNING", "DEBUG", "CRITICAL"
    :param filemode: The mode of the log file: "w", "a"
    :param handler: The handler to use
    :type filename: str
    :type loglevel: str
    :type filemode: str
    :type handler: logging.Handler
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
    :type message: str
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


class BootstraparseError(Exception):
    """
    Base class for all Bootstraparse errors
    """
    pass


class BootstraparseTokenError(BootstraparseError):
    """
    Error on a token, provides if possible the line and column number of the error,
    the file name and the message of the error
    and if possible a context for the error
    """
    def __init__(self, token, pile, message):
        self.token = token
        self.pile = pile
        if token is not None:
            self.line = token.line_number
            self.index = token.index
            self.label = token.label
            self.name = token.file_name
        else:
            self.line = None
            self.index = None
            self.label = None
            self.name = None
        self.context = self.get_context()
        super().__init__(message+"\n"+self.context_multiline())

    def get_context(self, context_size=5):
        """
        Returns the context of the error
        :return: The context of the error
        :rtype: str
        """
        if self.pile:
            st = max(0, self.index - context_size)
            en = min(len(self.pile), self.index + context_size)
            return self.pile[st:en]
        return []

    def context_multiline(self, context_size=10):
        """
        Returns the context of the error as a multiline string
        :return: The context of the error
        :rtype: str
        """
        if self.pile:
            return "\n".join([
                f"{'  ' if i!=context_size else '> '}{i-context_size:2d}: {j}"
                for i, j in enumerate(self.get_context(context_size)) if j.label != "linebreak"
            ])
        return ""


class ParsingError(Exception):
    """
    Exception class for parsing errors
    """

    def __init__(self, message=None, line=None, column=None, file=None):
        """
        Initializes the ParsingError class with the filename and a line and column number
        based on the current position in the file (if available)
        :param message: The message to display
        :type message: str
        :param line: The line number of the error
        :type line: int
        :param column: The column number of the error
        :type column: int
        :param file: The name of the file
        :type file: str
        :return: None
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


class MismatchedContainerError(BootstraparseTokenError):
    """
    The token is not final and cannot be contained. Indicative of a mismatched token.
    """
    def __init__(self, token, pile=None):
        """
        Initializes the MismatchedContainerError class with the token that was not final
        :param token: The token that is not final
        :type token: syntax.SemanticType
        """
        self.token = token
        self.pile = pile
        if token:
            self.line = token.line_number
            self.label = token.label
            self.name = token.file_name
        else:
            self.line = None
            self.label = None
            self.name = None
        super().__init__(token, pile, f"Could not process {self.label} at line {self.line} in file {self.name}.")


class LonelyOptionalError(BootstraparseError):
    """
    Optional token could not be matched with last element in pile (not a container).
    """
    def __init__(self, token, last_in_pile):
        """
        Initializes the LonelyOptionalError class with the token found and the last element in the pile
        Used when a token is found that is optional and cannot be matched with the last element in the pile (not a container)
        :param token: The token that is not final
        :type token: syntax.SemanticType
        :param last_in_pile: The last element in the pile
        :type last_in_pile: syntax.SemanticType
        """
        self.token = token
        if token:
            self.line = token.line_number
            self.label = token.label
            self.name = token.file_name
        else:
            self.line = None
            self.label = None
            self.name = None
        if last_in_pile:
            super().__init__(f"Could not match token {token} at line {self.line} with "
                             f"last element in pile {last_in_pile} at line {last_in_pile.line_number} "
                             f"in file {self.name}(not a container).")
        else:
            super().__init__(f"Could not match token {token} at line {self.line} in file {self.name}"
                             f"as there was nothing in the pile.")
