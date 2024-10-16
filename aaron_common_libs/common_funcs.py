"""Aaron's Common Functions."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from json import dumps as json_dumps
from logging import getLogger
from os.path import exists
from textwrap import dedent

from config import Config
from tablib import Dataset

logger = getLogger("default")

config = Config()


def ask(question, default="no"):
    """Ask a yes/no question via input() and return the answer.

    Args:
        question (str): The question to present to the user.
        default (str, optional): The presumed answer if the user just hits <Enter>.
                                 It must be "yes", "no", or None (meaning an answer
                                 is required from the user). Defaults to "no".

    Returns:
        bool: True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    prompts = {None: " [y/n] ", "yes": " [Y/n] ", "no": " [y/N] "}

    if default not in prompts:
        raise ValueError(f"invalid default answer: '{default}'")

    prompt = prompts[default]

    while True:
        choice = input(question + prompt).lower()
        if choice in valid:
            return valid[choice]
        if choice == "" and default is not None:
            return valid[default]
        print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def find_diff_in_lists(first_list=None, second_list=None):
    """Find the difference between two lists.

    Args:
        first_list (list): The first list.
        second_list (list): The second list.

    Returns:
        diff_list (list): A list of differences between first_list and second_list.
    """
    diff_list = [item for item in first_list if item not in second_list]
    return diff_list


def pad_string(string, length):
    """Add whitespace to a string to achieve desired string length.

    Args:
        string (str): The string to pad.
        length (int): The desired string length.

    Returns:
        padded_string (str): Padded string.
    """
    if len(string) < length:
        padded_string = string.ljust(length)
    else:
        padded_string = string[:length]
    return padded_string


def pretty_print(this_obj):
    """Return a nicely-formatted JSON string, with support for class objects.

    Args:
        this_obj (any): The object (dict, list, or class instance) to be converted to a pretty-printed JSON string.

    Returns:
        str: A JSON-formatted string with indentation for readability.
    """

    def class_to_dict(obj):
        """Custom serializer function to handle class objects."""
        # If the object has a `to_dict()` method, use it to convert to a dictionary
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        # Otherwise, raise a TypeError to let JSON know it's not serializable
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    return json_dumps(this_obj, indent=4, default=class_to_dict)


def write_to_csv(csv_filename, csv_headers, this_json):
    """Write JSON to CSV.

    Args:
        csv_filename (str): The name of the CSV file.
        csv_headers (list): A list containing the names of the headers in the CSV file.
        this_json (dict): The dictionary to be written to CSV file.

    Returns:
        write_success (bool): True if the CSV file was written successfully.
    """
    logger.debug("csv_filename==%s", csv_filename)
    logger.debug("csv_headers==%s", csv_headers)
    logger.debug("this_json==%s", this_json)
    try:
        if exists(path=csv_filename):
            with open(file=csv_filename, mode="a", encoding="utf-8") as csv_file:
                data = Dataset()
                temp_list = []
                for key, _ in this_json.items():
                    temp_list.append(this_json[key])
                data.append(temp_list)
                csv_file.write(data.export("csv"))
        else:
            with open(file=csv_filename, mode="w", encoding="utf-8") as csv_file:
                data = Dataset(headers=csv_headers)
                temp_list = []
                for key, _ in this_json.items():
                    temp_list.append(this_json[key])
                data.append(temp_list)
                csv_file.write(data.export("csv"))
        write_success = True
    except Exception as some_exception:  # pylint: disable=broad-except
        logger.error("ERROR==%s", some_exception)
        write_success = False
    return write_success


cli = ArgumentParser(
    formatter_class=RawDescriptionHelpFormatter,
    description=dedent(
        f"""\
        {config.app_dict["title"]} v{config.app_dict["version"]} ({config.app_dict["date"]})
        --
        Description: {config.app_dict["desc"]}
        Author:      {config.app_dict["author"]}
        URL:         {config.app_dict["url"]}"""
    ),
)
subparsers = cli.add_subparsers(dest="subcommand")


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the subcommand decorator."""
    return list(name_or_flags), kwargs


def subcommand(args=None, parent=subparsers):
    """Decorator to define a new subcommand in a sanity-preserving way.

    https://gist.github.com/mivade/384c2c41c3a29c637cb6c603d4197f9f
    The function will be stored in the ``func`` variable when the parser
    parses arguments so that it can be called directly like so::

        args = cli.parse_args()
        args.func(args)

    Usage example::

        @subcommand([argument("-d", help="Enable debug mode", action="store_true")])
        def subcommand(args):
            print(args)

    Then on the command line::

        $ python cli.py subcommand -d

    """

    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator
