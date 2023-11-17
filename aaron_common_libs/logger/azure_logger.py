"""Custom Class for sending log messages to Azure Blob Storage."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Code borrowed from: https://stackoverflow.com/questions/76263069/python-logging-with-custom-handler-for-azure-blob-storage-on-the-root-logger

from logging import Handler

from azure.storage.blob import ContentSettings


class AzureBlobStorageHandler(Handler):
    """Custom Class to handle custom Azure Handlers for logging."""

    def __init__(self, container_client, log_filename=None):
        """Initializes the custom logging handler."""
        super().__init__()
        self.blob_name = log_filename
        self.container_client = container_client
        self.blob_client = container_client.get_blob_client(self.blob_name)
        if not self.blob_client.exists():
            self.create_blob()

    def create_blob(self):
        """Create a new blob if one doesn't already exist."""
        # Create a blob client for the log record
        content_settings = ContentSettings(content_type="text/plain")
        self.blob_client.create_append_blob(content_settings)

    def emit(self, record):
        """This function gets called when a log event gets emitted.

        It receives a record, formats it and sends it to the url.
        """
        log_data = self.format(record).encode("utf-8")
        self.blob_client.append_block(f"{log_data}\n")
