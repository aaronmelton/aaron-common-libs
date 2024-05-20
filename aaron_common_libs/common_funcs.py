"""Aaron's Common Functions."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
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
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"invalid default answer: '{default}'")

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":  # pylint: disable=no-else-return
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("""Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n""")


def find_diff_in_lists(first_list=None, second_list=None):
    """Find the difference between two lists.

    Args
    ----
    first_list: list
    second_list: list

    Returns
    -------
    diff_list: list
    """
    # logger.debug("first_list==%s", first_list)
    # logger.debug("second_list==%s", second_list)
    diff_list = [item for item in first_list if item not in second_list]
    # logger.debug("diff_list==%s", diff_list)
    return diff_list


def pretty_print(this_dict):
    """Return a nicely-formatted JSON string.

    Args
    ----
    this_dict: dict

    Returns
    -------
    json_dumps: dict
    """
    return json_dumps(this_dict, indent=4)


def write_to_csv(csv_filename, csv_headers, this_json):
    """Write JSON to CSV.

    Args
    ----
    csv_filename: str
    csv_headers: list
    this_json: dict

    Returns
    -------
    write_success: bool
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


# pylint: disable=dangerous-default-value
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
