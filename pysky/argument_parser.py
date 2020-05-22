"""This module is called after utils/prefs and parses the passed CLI options"""
import os
from pathlib import Path
import argparse
from datetime import date, timedelta
from astropy import time as atime
from .const import Const

def cli_parse() -> tuple:
    """
    Parse the given arguments and return the start and end time objects
    :return: astropy.time objects
    """
    parser = argparse.ArgumentParser(
        description='pysky is an interactive module that allows the ' +
        'user to check the sky given a date and time allowing them ' +
        'to know what where be visible and where in the sky the ' +
        'objects will be located. Giving no options will run the ' +
        'progam in GUI mode.'
    )
    parser.add_argument(
        '-sd',
        '--startdate',
        help='Starting date if no other arguments ' +
        'give, it defaults to one hour.',
        type=str
    )
    parser.add_argument(
        '-st',
        '--starttime',
        help='Starting time.',
        type=str
    )
    parser.add_argument(
        '-ed',
        '--enddate',
        help='Ending date.',
        type=str
    )
    parser.add_argument(
        '-et',
        '--endtime',
        help='Ending time.',
        type=str
    )
    parser.add_argument(
        '-t',
        '--threads',
        help='Number of threads to run this program with.',
        default=1,
        type=int
    )
    parser.add_argument(
        '-v',
        '--verbosity',
        help='Verbosity level (1, 2, 3, 4, 5)',
        default=2,
        type=int
    )

    args = parser.parse_args()

    # Sets the number of threads
    Const.THREADS = args.threads

    # Sets the verbosity level
    if args.verbosity == 1:
        Const.VERBOSITY = 50

    elif args.verbosity == 2:
        Const.VERBOSITY = 40

    elif args.verbosity == 3:
        Const.VERBOSITY = 30

    elif args.verbosity == 4:
        Const.VERBOSITY = 20

    elif args.verbosity == 5:
        Const.VERBOSITY = 10

    else:
        Const.VERBOSITY = 0

    # Enter GUI mode
    if args.startdate is None and args.starttime is None:
        gui_launch()

    # Enter one hour mode
    if (
            (args.startdate is not None)
            and (args.starttime is not None)
            and (args.enddate is None)
            and (args.endtime is None)
    ):
        # Call to just run the module for one hour
        return one_hour_mode(args.startdate, args.starttime)

    if (
            (args.startdate is not None)
            and (args.starttime is not None)
            and (args.enddate is not None)
            and (args.endtime is not None)
    ):
        a_start = atime.Time(f"{args.startdate} {args.starttime}")
        a_end = atime.Time(f"{args.enddate} {args.endtime}")
        return a_start, a_end


def gui_launch():
    """Launch the GUI mode if there are no args or issues with given args."""
    exit()


def one_hour_mode(sdate: str, stime: str) -> tuple:
    """
    Generate end date and time.
    :param sdate: Start date arguemnt.
    :param stime: Start time argument.
    :return: Tuple of astropy.time objects.
    """
    # Adding an hour changes the date and time
    if int(stime.split(":")[0]) == 23:

        # Rest the hour to 00 (12 AM)
        etime = f"00:{stime.split(':')[1]}"

        # Increment the date by 1 day
        edate = date(
            year=int(sdate.split("-")[0]),
            month=int(sdate.split("-")[1]),
            day=int(sdate.split("-")[2])
        ) + timedelta(days=1)
        a_start = atime.Time(f"{sdate} {stime}")
        a_end = atime.Time(f"{edate} {etime}")
        return a_start, a_end

    etime = f"{int(stime.split(':')[0]) + 1}:{stime.split(':')[1]}"
    a_start = atime.Time(f"{sdate} {stime}")
    a_end = atime.Time(f"{sdate} {etime}")
    return a_start, a_end


def print_help():
    """
    Print out README when there is an issue with the args.
    """
    root_dir = Path(os.path.dirname(os.path.realpath((__file__)))).parent
    with open(f"{root_dir}/README.rst", "r") as help_file:
        for line in help_file.readlines():
            print(line.rstrip())
