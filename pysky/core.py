import json
import os.path

import astropy

import astroplan
from astroplan import download_IERS_A
from .argument_parser import cli_parse
from .astro_info import get_ephemeries_info
from .objectfilter import emphemeries_filter
from .prefs import check_integrity
from .skyview import get_skyview_img


def invoke(cli_args):
    """
    This is the main function that calls all other relevant functions
    :param root_dir: absolute path to this file
    """
    root_dir = os.path.abspath(os.path.dirname(__file__))

    cli_parse(root_dir, cli_args)
    hawthorn_hollow = astroplan.Observer(
        location=astropy.coordinates.EarthLocation.from_geodetic(
            -87.8791 * astropy.units.deg,
            42.6499 * astropy.units.deg,
            height=204 * astropy.units.m,
        ),
        name="Hawthorn Hollow",
        timezone="US/Central",
    )

    check_integrity(root_dir)

    celestial_objs = emphemeries_filter(
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
        get_skyview_img(celestial_obj, 1080, 1080, 3.5, "Linear", root_dir)

    # Open cache file
    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())

    # Iterate through the ephemeries to add information
    for body in EPHEMERIES_BODIES:
        cache_file = get_ephemeries_info(EPHEMERIES_BODIES, root_dir, cache_file)
    # Dump cache file
    with open(f"{root_dir}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)
