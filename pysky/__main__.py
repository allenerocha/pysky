#!/usr/bin/env python3
# encoding: utf-8
"""The main entry point. Invoke as `pysky'.
"""
import json
import os.path
import sys
import time

import astropy

import astroplan
import pysky.utils.astro_info
import pysky.utils.check_sky
import pysky.utils.cli
import pysky.utils.image_manipulation
import pysky.utils.objectfilter
import pysky.utils.prefs
import pysky.utils.skyview
from astroplan import download_IERS_A


def main(root_dir: str, location: object):
    """
    This is the main function that calls all other relevant functions
    :param root_dir: absolute path to this file
    """

    pysky.utils.prefs.check_integrity(root_dir)

    celestial_objs = pysky.utils.objectfilter.emphemeries_filter(
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

    # Iterate STARS to get images and data
    for celestial_obj in STARS:
        # Call to download images
        pysky.utils.skyview.get_img(celestial_obj, 1080, 1080, 3.5, "Linear", root_dir)

    # Open cache file
    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())

    # Iterate through the ephemeries to add information
    for body in EPHEMERIES_BODIES:
        # COORDS = utils.astro_info.get_info(root_dir, body)
        cache_file = pysky.utils.astro_info.get_ephemeries_info(
            EPHEMERIES_BODIES, root_dir, cache_file
        )
    # Dump cache file
    with open(f"{root_dir}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)


if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.dirname(__file__))

    viewing_time_range = pysky.utils.cli.parse(root_dir, sys.argv[1:])
    hawthorn_hollow = astroplan.Observer(
        location=astropy.coordinates.EarthLocation.from_geodetic(
            -87.8791 * astropy.units.deg,
            42.6499 * astropy.units.deg,
            height=204 * astropy.units.m,
        ),
        name="Hawthorn Hollow",
        timezone="US/Central",
    )
    main(root_dir, hawthorn_hollow)
