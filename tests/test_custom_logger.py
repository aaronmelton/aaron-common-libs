"""Test class CustomLogger."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pylint: disable=invalid-name, duplicate-code

import logging
from pathlib import Path

import pytest
from aaron_common_libs.logger.custom_logger import CustomLogger  # Import your CustomLogger class


@pytest.fixture(name="log_dict")
def fixture_log_dict():
    """Fixture to provide a sample logging configuration dictionary."""
    return {"level": "ERROR", "filename": "./logs/test_log.log", "path": "./logs"}


@pytest.fixture(name="custom_logger")
def fixture_custom_logger(log_dict):
    """Fixture to create an instance of CustomLogger."""
    return CustomLogger(log_dict)


def test_initialization(custom_logger):
    """Test that the CustomLogger is initialized correctly."""
    assert custom_logger is not None
    assert custom_logger.all is not None
    assert custom_logger.default is not None
    assert isinstance(custom_logger.all, logging.Logger)
    assert isinstance(custom_logger.default, logging.Logger)


def test_log_file_creation(custom_logger, log_dict):
    """Test that the log file is created and messages are logged correctly."""
    log_file_path = Path(log_dict["filename"])
    custom_logger.default.error("Test error message")
    assert log_file_path.exists(), f"Log file {log_file_path} was not created"
    with log_file_path.open(encoding="utf-8") as log_file:
        logs = log_file.read()
        assert "Test error message" in logs, "Log message not found in log file"


def test_log_format(custom_logger, log_dict):
    """Test that log messages are correctly formatted."""
    log_file_path = Path(log_dict["filename"])
    custom_logger.default.error("Test format message")
    with log_file_path.open(encoding="utf-8") as log_file:
        logs = log_file.read()
        assert "Log Level: ERROR" in logs, "Log level not found in log file"
        assert "Test format message" in logs, "Log message not found in log file"


def test_console_logging(custom_logger, caplog):
    """Test that log messages are written to the console."""
    with caplog.at_level(logging.ERROR):
        custom_logger.default.error("Test console message")

    # Check if the log message appears in the captured logs
    assert "Test console message" in caplog.text, "Console message not found in output"


def test_logger_configuration(custom_logger):
    """Test that the loggers are configured with the correct log level."""
    assert custom_logger.all.level == logging.ERROR, "Logger 'all' has incorrect log level"
    assert custom_logger.default.level == logging.ERROR, "Logger 'default' has incorrect log level"


def test_create_log_directory(log_dict):
    """Test that the log directory is created if it does not exist."""
    log_dir = Path(log_dict["path"])
    if log_dir.exists():
        for file in log_dir.iterdir():
            file.unlink()
        log_dir.rmdir()
    assert not log_dir.exists(), "Log directory already exists"
    CustomLogger(log_dict)
    assert log_dir.exists(), "Log directory was not created"
