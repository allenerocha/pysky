#!/usr/bin/env python3
# encoding: utf-8
import json
import os.path
import sys
import time

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


def main():
    """
    """
    utils.prefs.check_integrity()

    utils.prefs.clean_cache()

    celestial_objs = utils.objectfilter.emphemeries_filter(
        "venus", "polaris", "neptune", "vega", "saturn", "deneb", "sirius", "capella"
    )
    STARS = celestial_objs[0]
    EPHEMERIES_BODIES = celestial_objs[1]

    db_calls(STARS)

    # todo overlay celesital statistics on the image <==== WIP
    # todo add overlayed image to slideshow queue
    # todo play slideshow *****
    # todo make sure not to repeatedly add object information if it is already stored in the cache ******

    # Checks in the passed body or list of bodies are in the emphemeries Quantity

    # Open cache file
    cache_file = json.loads(open("data/cache", "r").read())

    # Iterate through the ephemeries to add information
    for body in EPHEMERIES_BODIES:
        COORDS = utils.astro_info.get_info(body)
        cache_file = get_ephemeries_info(EPHEMERIES_BODIES, cache_file)
    # Dump cache file
    with open("data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)


def db_calls(celestial_objs):
    # Iterate STARS to get images and data
    for celestial_obj in celestial_objs:
        # Call to download images
        utils.skyview.get_img(celestial_obj, 480, 480, 3.5, "Linear")
        # cache_file = json.loads(open("data/cache", "r").read())
        utils.prefs.clean_cache()


def get_ephemeries_info(bodies: list, cache_file: dict) -> dict:
    # Iterate through the ephemeries to add information
    for body in bodies:
        COORDS = utils.astro_info.get_info(body)
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
    viewing_time_range = utils.cli.parse(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    )
    earth_loc = astroplan.Observer(
        location=astropy.coordinates.EarthLocation.from_geodetic(
            -87.8791 * astropy.units.deg,
            42.6499 * astropy.units.deg,
            height=204 * astropy.units.m,
        ),
        name="Schoolyard Observatory",
        timezone="US/Central",
    )
    main()
