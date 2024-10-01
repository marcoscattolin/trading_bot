#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

import logging
import os
import uuid
from logging import handlers

from src import ROOT_DIR

LOGS = "logs"


class PathConfig:
    """
    Class to load path configuration for log files
    """

    def __init__(self):
        # id
        self.run_id = uuid.uuid4()

        # logs
        self.log_path = os.path.join(ROOT_DIR, LOGS)

        os.makedirs(self.log_path, exist_ok=True)


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter to add colors to console logs based on the log level.
    """

    COLOR_CODES = {
        logging.DEBUG: "\033[95m",  # Magenta
        logging.INFO: "\033[96m",  # Cyan
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[91m",  # Red
    }

    def format(self, record):
        color_code = self.COLOR_CODES.get(record.levelno, "")
        reset_code = "\033[0m"
        message = super().format(record)
        return f"{color_code}{message}{reset_code}"


def get_logger(conf: PathConfig, log_level=logging.WARNING) -> logging.Logger:
    """
    Method initializing logger

    :param conf: PathConfig object containing logging path configuration
    :param log_level: level at which logs are produced, defaults to warning
    :return: logger to be used when logging messages

    """
    # define log filename
    logfile = f"{conf.log_path}/logfile.log"

    # Define formats
    console_format = (
        "[%(asctime)s][%(name)s][%(funcName)s:%(lineno)d][%(levelname)s] %(message)s"
    )
    file_format = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    # init logger
    logger = logging.getLogger(str(conf.run_id))
    logger.setLevel(log_level)

    # Add rotating logfile handler (max 5 backups, 1 megabyte each)
    rotating_handler = handlers.RotatingFileHandler(
        logfile, maxBytes=10**6, backupCount=5
    )
    file_formatter = logging.Formatter(file_format, datefmt)
    rotating_handler.setFormatter(file_formatter)
    logger.addHandler(rotating_handler)

    # add console handler
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(console_format, datefmt)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger


# init path configuration
path_conf = PathConfig()
logger = get_logger(conf=path_conf, log_level=logging.DEBUG)

# print debug messages
logger.debug(f"Logging into {path_conf.log_path}")
