"""This module continas all functions related to filtering
out all stars from planets and deep space objects"""
from .logger import Logger

from .astro_info import get_bodies


def emphemeries_filter(args: list) -> tuple:
    """
    This function takes the passed list and filters
    out all the ephemeries bodies into another list.
    :param arg: List of passed bodies.
    :return: tuple of objects filtered and sperated.
    """
    Logger.log("Filtering objects.")
    # Converts tuple to list
    celestial_objs = args

    # Retrieves a list of all ephemeriers bodies in that list
    EPHEMERIES_BODIES = get_bodies(args)

    # Removes all ephemeries bodies from the list
    STARS = [
        celestial_obj
        for celestial_obj in celestial_objs
        if celestial_obj not in EPHEMERIES_BODIES
    ]
    Logger.log("Filtering complete.\n")
    return STARS, EPHEMERIES_BODIES
