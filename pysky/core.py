import json
import logging
import os.path
from logging import critical
from pathlib import Path

import astropy

import astroplan
from astroplan import download_IERS_A

from .argument_parser import cli_parse
from .astro_info import get_ephemeries_info
from .catalog_parse import parse_cadwell, parse_messier
from .check_sky import is_object_visible
from .objectfilter import emphemeries_filter
from .prefs import check_integrity, read_user_prefs
from .skyview import get_skyview_img


def invoke(cli_args):
    """
    This is the main function that calls all other relevant functions
    :param root_dir: absolute path to this file
    """
    root_dir = os.path.abspath(os.path.dirname(__file__))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    START_TIME, END_TIME = cli_parse(root_dir, cli_args)

    HAWTHORN_HOLLOW = astroplan.Observer(
        location=astropy.coordinates.EarthLocation.from_geodetic(
            -87.8791 * astropy.units.deg,
            42.6499 * astropy.units.deg,
            height=204 * astropy.units.m,
        ),
        name="Hawthorn Hollow",
        timezone="US/Central",
    )

    check_integrity(root_dir)
    CADWELL_OBJECTS = parse_cadwell(root_dir)
    MESSIER_OBJECTS = parse_messier(root_dir)
    USER_OBJECTS = read_user_prefs(root_dir)

    celestial_objs = emphemeries_filter(root_dir, USER_OBJECTS)
    STARS = celestial_objs[0]
    EPHEMERIES_BODIES = celestial_objs[1]
    # Calls the skyview api and simbad
    # api and returns the the list of stars
    STARS = invoke_skyview(STARS, root_dir)
    # Open cache file
    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())

    # Iterate through the ephemeries to add information
    for body in EPHEMERIES_BODIES:
        cache_file = get_ephemeries_info(EPHEMERIES_BODIES, root_dir, cache_file)
    # Dump cache file
    with open(f"{root_dir}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)

    cached_visible = get_visible(START_TIME, END_TIME, HAWTHORN_HOLLOW)
    messier_visible = get_visible(
        START_TIME,
        END_TIME,
        HAWTHORN_HOLLOW,
        celestial_objs=list(MESSIER_OBJECTS.keys()),
    )
    cadwell_visible = get_visible(
        START_TIME,
        END_TIME,
        HAWTHORN_HOLLOW,
        celestial_objs=list(CADWELL_OBJECTS["NGC number"].keys()),
    )


def invoke_skyview(stars, root_dir):
    del_stars = list()
    # Iterate STARS to get images and data
    for celestial_obj in stars:
        STATUS_CODE = get_skyview_img(
            celestial_obj, 1080, 1080, 3.5, "Linear", root_dir
        )
        # Call to download images
        if STATUS_CODE == 1:
            critical(
                f"Brightness of {celestial_obj} is below 4.5! Removing from queue..."
            )
            del_stars.append(celestial_obj)
        elif STATUS_CODE == 2:
            critical(
                f"Error downloading webpage for {celestial_obj}! Removing from queue..."
            )
            del_stars.append(celestial_obj)
        elif STATUS_CODE == 3:
            critical(
                f"Error trying to parse the web page of {celestial_obj}! Removing from queue..."
            )
            del_stars.append(celestial_obj)
        elif STATUS_CODE == 4:
            continue
        else:
            critical(
                f"Ran into an unknown error please create a issue on:\nhttps://github.com/allenerocha/pysky/issues/new\n! Removing {celestial_obj} from queue..."
            )
            del_stars.append(celestial_obj)

    return list(set(del_stars) ^ set(stars))


def get_visible(start_time, end_time, location, celestial_objs=None) -> dict():
    visible = dict()
    if celestial_objs is None:
        cache_file = json.loads(
            open(
                f"{Path(os.path.dirname(os.path.realpath((__file__))))}/data/cache",
                "r",
            ).read()
        )
        celestial_objs = cache_file.keys()

    for celestial_obj in celestial_objs:
        try:
            obj = astroplan.FixedTarget.from_name(celestial_obj)
            alt, az, t = is_object_visible(obj, start_time, end_time, location)
            visible[celestial_obj] = {
                "altitude": str(alt),
                "azimuth": str(az),
                "start time": str(t),
            }
        except astropy.coordinates.name_resolve.NameResolveError as e:
            print(str(e))
    return visible
