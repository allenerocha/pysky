"""This module is called after utils/prefs and parses the passed CLI options"""
import datetime
import logging
import sys
from logging import info
from pathlib import Path

import astropy.time


def cli_parse(root_dir: str, cli_args: list) -> list:
    """
    POSITION 0 & 2 (DATE)
    POSITION 1 & 3 (TIME)
    FORMATS:
        DATE:   YEAR-DAY-MON    (DIGITS)
        TIME:   HOUR:MINUTE     (DIGITS)
    """

    if not isinstance(root_dir, str) or len(root_dir) < 1:
        root_dir = Path(__file__).parent

    if not isinstance(cli_args, list):
        print_help()
        raise TypeError(
            f"Value passed to cli_parse must be a list not {type(cli_args)}."
        )

    if not len(cli_args) == 4:
        print_help()
        raise IndexError(f"Argument for cli_parse must be size 4 not {len(cli_args)}.")

    for arg in cli_args:
        if not isinstance(arg, str):
            print_help()
            raise TypeError(f"{arg} should be a string type not {type(arg)}.")
        if len(arg) < 1:
            raise IndexError(f"Arguments for cli_parse cannot be empty.")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )
    try:
        info("Parsing cli input...")
        year_one = int(cli_args[0].split("-")[0])
        month_one = int(cli_args[0].split("-")[2])
        day_one = int(cli_args[0].split("-")[1])
        hour_one = int(cli_args[1].split(":")[0])
        minute_one = int(cli_args[1].split(":")[1])

        datetime_one = datetime.datetime(
            year=year_one,
            month=month_one,
            day=day_one,
            hour=hour_one,
            minute=minute_one,
        )

        year_two = int(cli_args[2].split("-")[0])
        month_two = int(cli_args[2].split("-")[2])
        day_two = int(cli_args[2].split("-")[1])
        hour_two = int(cli_args[3].split(":")[0])
        minute_two = int(cli_args[3].split(":")[1])

        datetime_two = datetime.datetime(
            year=year_two,
            month=month_two,
            day=day_two,
            hour=hour_two,
            minute=minute_two,
        )
    except IndexError as e:
        print(str(e))
        print_help()
        sys.exit()

    START_TIME = astropy.time.Time(datetime_one)
    END_TIME = astropy.time.Time(datetime_two)

    return [START_TIME, END_TIME]


def print_help():
    with open(f"{Path(__file__).parent.parent}/README.rst", "r") as help_file:
        for line in help_file.readlines():
            print(line.rstrip())
