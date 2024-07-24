"""Test class AzureBlobStorageHandler."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pylint: disable=invalid-name, duplicate-code

import unittest.mock
from logging import Formatter, LogRecord

import pytest
from azure.storage.blob import BlobClient, ContainerClient

from aaron_common_libs.logger.azure_logger import AzureBlobStorageHandler


@pytest.fixture(name="container_client_fixture")
def fixture_container_client_fixture():
    """Fixture for mocking ContainerClient."""
    container_client = unittest.mock.MagicMock(spec=ContainerClient)
    return container_client


@pytest.fixture(name="blob_client_fixture")
def fixture_blob_client_fixture():
    """Fixture for mocking BlobClient."""
    blob_client = unittest.mock.MagicMock(spec=BlobClient)
    return blob_client


@pytest.fixture(name="handler_fixture")
def fixture_handler_fixture(container_client_fixture, blob_client_fixture):
    """Fixture for creating an instance of AzureBlobStorageHandler."""
    with unittest.mock.patch.object(container_client_fixture, "get_blob_client", return_value=blob_client_fixture):
        handler_instance = AzureBlobStorageHandler(container_client_fixture, "test_log.txt")
        return handler_instance


def test_initialization(handler_fixture, container_client_fixture, blob_client_fixture):
    """Test for correct initialization of the handler."""
    assert handler_fixture.blob_name == "test_log.txt"
    assert handler_fixture.container_client == container_client_fixture
    assert handler_fixture.blob_client == blob_client_fixture


def test_create_blob(handler_fixture, blob_client_fixture):
    """Test for the create_blob method."""
    handler_fixture.create_blob()
    blob_client_fixture.create_append_blob.assert_called_once()


def test_emit(handler_fixture, blob_client_fixture):
    """Test for the emit method."""
    log_record = LogRecord(
        name="test", level=20, pathname="test_path", lineno=10, msg="test message", args=(), exc_info=None
    )
    handler_fixture.setFormatter(Formatter("%(message)s"))

    handler_fixture.emit(log_record)

    formatted_log = "test message\n".encode("utf-8")
    blob_client_fixture.append_block.assert_called_once_with(formatted_log)
