"""This module continas all functions related to filtering out all stars from planets and deep space objects"""
import logging
from logging import info

import utils.astro_info


def emphemeries_filter(root_dir: str, *args) -> list:
    """
    This function takes the passed list and filters out all the ephemeries bodies into another list
    :param arg: List of passed bodies
    :return: [[STARS], [EPHEMERIES BODIES]]
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    info("Filtering objects.")
    # Converts tuple to list
    celestial_objs = list(args)

    # Retrieves a list of all ephemeriers bodies in that list
    EPHEMERIES_BODIES = utils.astro_info.get_bodies(root_dir, list(args))

    # Removes all ephemeries bodies from the list
    STARS = [
        celestial_obj
        for celestial_obj in celestial_objs
        if celestial_obj not in EPHEMERIES_BODIES
    ]
    info("Filtering complete.\n")
    return [STARS, EPHEMERIES_BODIES]
