"""This module is called after utils/prefs and parses the passed CLI options"""
import astropy.time

def cli_parse(*args) -> list:
    """
    POSITION 0 & 2 (DATE)
    POSITION 1 & 3 (TIME)
    FORMATS:
        DATE:   YEAR-DAY-MON    (DIGITS)
        TIME:   HOUR:MINUTE
    """

    START_TIME = astropy.time.Time(f"{args[0]} {args[1]}")
    END_TIME = astropy.time.Time(f"{args[2]} {args[3]}")
    return [START_TIME, END_TIME]

