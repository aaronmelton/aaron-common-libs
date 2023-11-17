"""Aaron's Custom Logging Class."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from json import dumps as json_dumps
from logging import getLogger
from logging.config import dictConfig
from os import environ as os_environ
from pathlib import Path

from azure.storage.blob import BlobServiceClient


class CustomLogger:  # pylint: disable=too-few-public-methods
    """Class for custom logging destinations."""

    def __init__(self, log_dict=None):
        """Initialize this class.

        Args
        ----
        log_dict: dict

        Returns
        -------
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

        if (
            os_environ.get("LOG_AZURE", None)
            and log_dict["storage_account_name"]
            and log_dict["storage_connection_string"]
            and log_dict["storage_container_name"]
        ):
            log_container_client = BlobServiceClient.from_connection_string(
                conn_str=log_dict["storage_connection_string"]
            ).get_container_client(log_dict["storage_container_name"])
            # Add new azure logging handler to config
            logging_config["handlers"]["azure"] = {
                "level": "INFO",
                "class": "aaron_common_libs.logger.azure_logger.AzureBlobStorageHandler",
                "container_client": log_container_client,
                "log_filename": log_dict["filename"],
                "formatter": "default",
            }
            # Add new azure config to existing handlers
            logging_config["loggers"]["all"]["handlers"] = ["azure", "console", "file"]
            logging_config["loggers"]["default"]["handlers"] = ["azure", "console", "file"]
            self.all = self.configure_logger(name="all", log_config=logging_config, log_dict=log_dict)
            self.default = self.configure_logger(name="azure", log_config=logging_config, log_dict=log_dict)
        else:
            self.all = self.configure_logger(name="all", log_config=logging_config, log_dict=log_dict)
            self.default = self.configure_logger(name="default", log_config=logging_config, log_dict=log_dict)

    def configure_logger(self, name, log_config, log_dict):
        """Configure multiple logging destinations.

        Args
        ----
        name: str
        log_config: dict
        log_dict: dict

        Returns
        -------
        log handler
        """
        Path(log_dict["path"]).mkdir(parents=True, exist_ok=True)
        dictConfig(config=log_config)
        return getLogger(name=name)
