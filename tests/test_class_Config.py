"""Test class Config."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pylint: disable=invalid-name, duplicate-code

from datetime import datetime
from re import match as re_match

from aaron_common_libs.config import Config


def test_config():
    """Test config.py"""
    config = Config()
    # Application Variables
    assert config.app_dict["author"] == "Aaron Melton <aaron@aaronmelton.com>"
    assert re_match("\\d{4}(-\\d{2}){2}", config.app_dict["date"])
    assert config.app_dict["desc"] == "meh."
    assert config.app_dict["title"] == "aaron_common_libs"
    assert config.app_dict["url"] == "https://github.com/aaronmelton/aaron_common_libs"
    assert re_match("\\d{1,2}(\\.\\d{1,2}){2}", config.app_dict["version"])

    # Logging Variables
    assert (
        config.log_dict["filename"]
        == f"""{config.log_dict["path"]}{config.app_dict["title"]}_{datetime.now().strftime("%Y%m%d")}.log"""
    )
    assert config.log_dict["level"] == "DEBUG"
    assert config.log_dict["path"] == "/tmp/"
