"""Main module that calls all relevant modules."""
import json
import os.path
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import astropy

import astroplan
from astroplan import download_IERS_A

from tqdm import tqdm

from .argument_parser import cli_parse
from .astro_info import get_ephemeries_info
from .catalog_parse import parse_caldwell, parse_messier
from .check_sky import is_object_visible
from .image_manipulation import overlay_text
from .objectfilter import emphemeries_filter
from .prefs import check_integrity, read_user_prefs
from .skyview import get_skyview_img
from .logger import Logger
from .const import Const
from .simbad import get_brightness, get_constellation, get_ra_dec


def invoke():
    """
    Call all other relevant functions.

    :param root_dir: absolute path to this file
    """
    download_IERS_A()

    START_TIME, END_TIME = cli_parse()

    HAWTHORN_HOLLOW = astroplan.Observer(
        location=astropy.coordinates.EarthLocation.from_geodetic(
            -87.8791 * astropy.units.deg,
            42.6499 * astropy.units.deg,
            height=204 * astropy.units.m,
        ),
        name="Hawthorn Hollow",
        timezone="US/Central",
    )

    check_integrity(Const.ROOT_DIR)
    CALDWELL_OBJECTS = parse_caldwell(Const.ROOT_DIR)
    MESSIER_OBJECTS = parse_messier(Const.ROOT_DIR)
    USER_OBJECTS = read_user_prefs(Const.ROOT_DIR)

    STARS, EPHEMERIES_BODIES = emphemeries_filter(USER_OBJECTS)

    # Calls the skyview api and simbad
    # api and returns the the list of stars
    invoke_skyview(STARS)
    # Open cache file
    cache_file = json.loads(open(f"{Const.ROOT_DIR}/data/cache", "r").read())
    for star in STARS:
        cache_file = get_br(star, cache_file)
        cache_file = get_cn(star, cache_file)
        cache_file = get_loc(star, cache_file)
    # Dump cache file
    with open(f"{Const.ROOT_DIR}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)
    cache_file = json.loads(open(f"{Const.ROOT_DIR}/data/cache", "r").read())

    set_img_txt(STARS)
    # Iterate through the ephemeries to add information
    for body in tqdm(EPHEMERIES_BODIES):
        cache_file = get_ephemeries_info(
            body,
            START_TIME,
            cache_file
        )

    # Dump cache file
    with open(f"{Const.ROOT_DIR}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)

    cached_visible = get_visible(
        START_TIME,
        END_TIME,
        HAWTHORN_HOLLOW,
        celestial_objs=STARS
    )
    messier_visible = get_visible(
        START_TIME,
        END_TIME,
        HAWTHORN_HOLLOW,
        celestial_objs=list(MESSIER_OBJECTS.keys()),
    )
    for m_obj in tqdm(messier_visible.keys()):
        static_data_path = (
            f"{os.path.abspath(os.path.dirname(__file__))}/data/static_data/"
        )
        Logger.log(f"Looking for {m_obj} in {static_data_path}...")
        for image in os.listdir(f"{static_data_path}"):
            if os.path.isfile(
                    f"{static_data_path}/{image}"
            ) and image.split(".")[0] == m_obj.replace(" ", ""):
                static_data_path += image
                Logger.log(
                    f"Found {m_obj} in {static_data_path}!"
                )
    set_img_txt(messier_visible.keys())

    caldwell_visible = get_visible(
        START_TIME,
        END_TIME,
        HAWTHORN_HOLLOW,
        celestial_objs=list(CALDWELL_OBJECTS["NGC number"].keys()),
    )
    for c_obj in tqdm(caldwell_visible.keys()):
        static_data_path = (
            f"{os.path.abspath(os.path.dirname(__file__))}/data/static_data/"
        )
        Logger.log(f"Looking for {c_obj} in {static_data_path}...")
        for image in os.listdir(f"{static_data_path}"):
            if os.path.isfile(
                f"{static_data_path}/{image}"
            ) and image.split(".")[0] == c_obj.replace(" ", ""):
                static_data_path += image
                Logger.log(f"Found {c_obj} in {static_data_path}!")
    set_img_txt(caldwell_visible.keys())


def set_simbad_values(celestial_obj: str, cache_file: dict):
    """
    Call the simbad module and get the brightness, constellation,
    and location.
    :param celestial_obj: Object to get values for.
    :param cache_file: Opened cache file to apply changes to.
    :return: Cache file with added simbad values.
    """
    cache_file[celestial_obj]["brightness"] = get_brightness(celestial_obj)

    cache_file[celestial_obj]["constellation"] = get_constellation(
        celestial_obj
    )

    ra_dec = get_ra_dec(celestial_obj)
    cache_file[celestial_obj]["coordinates"] = {
        "ra": ra_dec[0],
        "dec": ra_dec[1]
    }
    return cache_file


def invoke_skyview(stars):
    """Run skyview in as many threads as specified."""
    with ThreadPoolExecutor(max_workers=Const.THREADS) as executor:
        executor.map(get_skyview_img, stars)


def set_img_txt(celestial_objs):
    """Set the text on the image of the object."""
    with ThreadPoolExecutor(max_workers=Const.THREADS) as executor:
        executor.map(overlay_text, celestial_objs)


def get_visible(start_time, end_time, location, celestial_objs=None) -> dict:
    visible = dict()
    if celestial_objs is None:
        cache_file = json.loads(
            open(
                f"{Path(os.path.dirname(os.path.realpath((__file__))))}" +
                "/data/cache",
                "r",
            ).read()
        )
        celestial_objs = cache_file.keys()
    for celestial_obj in tqdm(celestial_objs):
        Logger.log(
            "Gathering name, start_altaz.alt, and start_altaz.az for " +
            f"{celestial_obj}..."
        )
        try:
            obj = astroplan.FixedTarget.from_name(celestial_obj)
            alt, azimuth, obj_time = is_object_visible(
                obj,
                start_time,
                end_time,
                location
            )
            visible[celestial_obj] = {
                "altitude": str(alt),
                "azimuth": str(azimuth),
                "start time": str(obj_time),
            }
            Logger.log(f"Sucessfully gathered data for {celestial_obj}!\n")
        except astropy.coordinates.name_resolve.NameResolveError as e:
            Logger.log(
                "Unabale to gather name, start_altaz.alt, and start_altaz.az" +
                f" for {celestial_obj}!\n", 40
            )
            Logger.log(str(e), 40)
    return visible
