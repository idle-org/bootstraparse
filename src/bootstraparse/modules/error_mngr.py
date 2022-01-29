# Dedicated module for defining and interpreting errors as well as generating error messages

import logging


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


def initlogging(filename=None, loglevel="ERROR"):
    """
    Initializes logging
    """
    loglevel = loglevel.upper()
    if loglevel not in ["ERROR", "INFO", "WARNING", "DEBUG", "CRITICAL"]:
        print("Incorrect logging", loglevel + ". Defaulting to ERROR.")
        loglevel = "ERROR"
    logging.basicConfig(encoding="utf-8")
    if filename is not None:
        logging.basicConfig(filename=filename)
    logging.basicConfig(level=logging.__getattribute__(loglevel))
