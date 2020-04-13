"""This module is called after utils/prefs and parses the passed CLI options"""
import datetime
import logging
from logging import info

import astropy.time


def parse(root_dir, *args) -> list:
    """
    POSITION 0 & 2 (DATE)
    POSITION 1 & 3 (TIME)
    FORMATS:
        DATE:   YEAR-DAY-MON    (DIGITS)
        TIME:   HOUR:MINUTE     (DIGITS)
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    info("Parsing cli input...")
    year_one = int(args[0].split("-")[0])
    month_one = int(args[0].split("-")[2])
    day_one = int(args[0].split("-")[1])
    hour_one = int(args[1].split(":")[0])
    minute_one = int(args[1].split(":")[1])

    datetime_one = datetime.datetime(
        year=year_one, month=month_one, day=day_one, hour=hour_one, minute=minute_one
    )

    year_two = int(args[2].split("-")[0])
    month_two = int(args[2].split("-")[2])
    day_two = int(args[2].split("-")[1])
    hour_two = int(args[3].split(":")[0])
    minute_two = int(args[3].split(":")[1])

    datetime_two = datetime.datetime(
        year=year_two, month=month_two, day=day_two, hour=hour_two, minute=minute_two
    )

    START_TIME = astropy.time.Time(datetime_one)
    END_TIME = astropy.time.Time(datetime_two)

    info("Successfully parsed cli input!\n")

    return [START_TIME, END_TIME]
