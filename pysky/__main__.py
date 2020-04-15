#!/usr/bin/env python3
# encoding: utf-8
"""The main entry point. Invoke as `pysky'.
"""
import json
import os.path
import sys
import time
from pathlib import Path

import astropy

import astroplan
import utils.astro_info
import utils.check_sky
import utils.cli
import utils.image_manipulation
import utils.objectfilter
import utils.prefs
import utils.skyview
from astroplan import download_IERS_A


def main(root_dir: str, location: object):
    """
    This is the main function that calls all other relevant functions
    :param root_dir: absolute path to this file
    """

    utils.prefs.check_integrity(root_dir)

    celestial_objs = utils.objectfilter.emphemeries_filter(
        root_dir,
        "venus",
        "polaris",
        "neptune",
        "vega",
        "saturn",
        "deneb",
        "sirius",
        "capella",
    )
    STARS = celestial_objs[0]
    EPHEMERIES_BODIES = celestial_objs[1]

    db_calls(STARS, root_dir)

    # Open cache file
    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())

    # Iterate through the ephemeries to add information
    for body in EPHEMERIES_BODIES:
        COORDS = utils.astro_info.get_info(root_dir, body)
        cache_file = get_ephemeries_info(EPHEMERIES_BODIES, cache_file)
    # Dump cache file
    with open(f"{root_dir}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)


def db_calls(celestial_objs, root_dir):
    # Iterate STARS to get images and data
    for celestial_obj in celestial_objs:
        # Call to download images
        utils.skyview.get_img(celestial_obj, 480, 480, 3.5, "Linear", root_dir)
        # cache_file = json.loads(open("data/cache", "r").read())


def get_ephemeries_info(bodies: list, cache_file: dict) -> dict:
    # Iterate through the ephemeries to add information
    for body in bodies:
        COORDS = utils.astro_info.get_info(root_dir, body)
        cache_file[f"{body}"] = {}
        cache_file[f"{body}"]["type"] = "planet"
        cache_file[f"{body}"]["created"] = time.strftime(
            "%Y-%d-%m %H:%M", time.gmtime()
        )
        cache_file[f"{body}"]["coordinates"] = {  # Right acension
            "ra": [str(COORDS[0]), str(COORDS[1]), str(COORDS[2])],
            "dec": str(COORDS[3]),
            "cartesian": [str(COORDS[5]), str(COORDS[6]), str(COORDS[7])],
        }
    return cache_file


if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.dirname(__file__))

    if "help" in sys.argv or "--help" in sys.argv or "-h" in sys.argv:
        with open(f"{Path(root_dir).parent}/README.md", "r") as help_file:
            for line in help_file.readlines():
                print(line.rstrip())
        sys.exit()

    viewing_time_range = utils.cli.parse(
        root_dir, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    )
    earth_loc = astroplan.Observer(
        location=astropy.coordinates.EarthLocation.from_geodetic(
            -87.8791 * astropy.units.deg,
            42.6499 * astropy.units.deg,
            height=204 * astropy.units.m,
        ),
        name="Hawthorn Hollow",
        timezone="US/Central",
    )
    main(root_dir, earth_loc)
