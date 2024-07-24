"""Aaron's Custom Logging Class."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from json import dumps as json_dumps
from logging import getLogger
from logging.config import dictConfig
from pathlib import Path


class CustomLogger:  # pylint: disable=too-few-public-methods
    """Class for custom logging destinations."""

    def __init__(self, log_dict=None):
        """Initialize this class.

        Args:
            log_dict (dict): Logging configuration dictionary.

        Returns:
            Object of Class
        """
        logging_config = {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "{asctime}  Log Level: {levelname:8}  Line: {lineno:4}  Function: {funcName:29}  Msg: {"
                    "message}",
                    "style": "{",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                },
                "json": {
                    "format": json_dumps(
                        {
                            "time": "%(asctime)s",
                            "log_level": "%(levelname)s",
                            "line": "%(lineno)s",
                            "function": "%(funcName)s",
                            "message": "%(message)s",
                        }
                    )
                },
            },
            "handlers": {
                "console": {
                    "level": "ERROR",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "level": log_dict["level"],
                    "class": "logging.FileHandler",
                    "formatter": "default",
                    "filename": log_dict["filename"],
                },
            },
            "loggers": {
                "all": {"level": log_dict["level"], "handlers": ["console", "file"]},
                "default": {"level": log_dict["level"], "handlers": ["console", "file"]},
            },
            "disable_existing_loggers": False,
        }

        self.all = self.configure_logger(name="all", log_config=logging_config, log_dict=log_dict)
        self.default = self.configure_logger(name="default", log_config=logging_config, log_dict=log_dict)

    def configure_logger(self, name, log_config, log_dict):
        """Configure multiple logging destinations.

        Args:
            name (str): Name of the logging handler (all, default, etc).
            log_config (dict): Custom logging handler configuration.
            log_dict (dict): Logging configuration dictionary.

        Returns:
            log handler
        """
        Path(log_dict["path"]).mkdir(parents=True, exist_ok=True)
        dictConfig(config=log_config)
        return getLogger(name=name)
