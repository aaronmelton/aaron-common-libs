"""Slack Messaging Functionality."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ChatGPT Conversation: https://chatgpt.com/share/673f39a8-52c4-8009-ab7a-5d75884884ca

from logging import getLogger
from typing import Dict, Optional

import requests

logger = getLogger("default")


class SlackMessenger:  # pylint: disable=too-few-public-methods
    """A simple library for sending messages to Slack.

    Attributes:
        webhook_url (str): The Slack webhook URL.
    """

    def __init__(self, webhook_url: str) -> None:
        """Initialize the SlackMessenger.

        Args:
            webhook_url (str): Slack webhook URL.
        """
        self.webhook_url = webhook_url

    def send_message(self, message: str, blocks: Optional[Dict] = None) -> bool:
        """Sends a message to Slack.

        Args:
            message (str): The message text.
            blocks (Optional[Dict]): A dictionary of Slack block elements for rich messaging (default: None).

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        payload = {"text": message}
        if blocks:
            payload["blocks"] = blocks

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Message sent to Slack successfully: %s", message)
            return True
        except requests.exceptions.RequestException as e:
            logger.error("Failed to send message to Slack: %s", e)
            return False


class SlackBotMessenger:  # pylint: disable=too-few-public-methods
    """A library for sending messages to Slack channels using a Slack bot token.

    Attributes:
        bot_token (str): The Slack bot token.
    """

    def __init__(self, bot_token: str) -> None:
        """Initialize the SlackBotMessenger.

        Args:
            bot_token (str): The Slack bot token.
        """
        self.bot_token = bot_token
        self.base_url = "https://slack.com/api/"

    def send_message(self, channel_id: str, message: str, blocks: Optional[Dict] = None) -> bool:
        """Sends a message to a Slack channel.

        Args:
            channel_id (str): The Slack channel ID.
            message (str): The message text.
            blocks (Optional[Dict]): A dictionary of Slack block elements for rich messaging (default: None).

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        url = f"{self.base_url}chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "channel": channel_id,
            "text": message,
        }
        if blocks:
            payload["blocks"] = blocks

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response_data = response.json()

            if not response_data.get("ok"):
                logger.error("Failed to send message to Slack. Error: %s", response_data.get("error"))
                return False

            logger.info("Message sent to Slack channel %s successfully: %s", channel_id, message)
            return True
        except requests.exceptions.RequestException as e:
            logger.error("Request failed: %s", e)
            return False
