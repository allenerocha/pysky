"""Main module that calls all relevant modules."""
import json
import os.path
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import astropy
from astropy.coordinates import SkyCoord
from tqdm import tqdm

from .argument_parser import cli_parse
from .astro_info import get_ephemeries_info
from .catalog_parse import parse_caldwell, parse_messier
from .check_sky import is_object_visible
from .const import Const
from .image_manipulation import overlay_text
from .jpl_horizons_query import ephemeries_query
from .logger import Logger
from .moonquery import query
from .output import to_html_list
from .prefs import check_integrity, read_user_prefs
from .simbad import get_brightness, get_constellation, get_distance, get_ra_dec
from .skyview import get_skyview_img

# Set up the thing to catch the warning (and potentially others)
with warnings.catch_warnings(record=True) as w:
    # import the modules
    import astroplan
    from astroplan import OldEarthOrientationDataWarning
    from astroplan import FixedTarget

    # One want to know aout the first time a warning is thrown
    warnings.simplefilter("once")

# Look through all the warnings to see if one
# is OldEarthOrientationDataWarning, update the table if it is.
for i in w:
    if i.category == OldEarthOrientationDataWarning:
        # This new_mess statement isn't really needed
        # I just didn't want to print all the
        # information that is produce in the warning.
        NEW_MESS = '.'.join(str(i.message).split('.')[:3])
        print('WARNING:', NEW_MESS)
        print('Updating IERS bulletin table...')
        from astroplan import download_IERS_A
        download_IERS_A()


def invoke():
    """
    Call all other relevant functions.
    """

    cli_parse()

    check_integrity()

    CALDWELL_OBJECTS = parse_caldwell(Const.ROOT_DIR)
    MESSIER_OBJECTS = parse_messier(Const.ROOT_DIR)
    USER_OBJECTS = read_user_prefs()

    gen_moon_data()

    STARS, EPHEMERIES = query_jpl_horizons(USER_OBJECTS)

    EPHEMERIES_BODIES = list(EPHEMERIES.keys())

    visible_objs = dict()
    for star in STARS:
        Logger.log(
            "Gathering zen, altitude, and " +
            f"azimuth for {star}..."
        )
        try:
            zen, altitude, azimuth = get_visible(
                star,
                3.0
            )
        except KeyError:
            continue
        if '' not in (zen, altitude, azimuth):
            Logger.log(f"Sucessfully gathered data for {star}!\n")
            visible = {str(star): dict()}
            visible[star]['Zenith'] = str(zen)
            visible[star]['Altitude'] = str(altitude)
            visible[star]['Azimuth'] = str(azimuth)
            visible_objs.update(visible)
    STARS = list(visible_objs.keys())
    # Calls the skyview api and simbad
    # api and returns the the list of stars
    invoke_skyview(STARS)
    # Open cache file
    cache_file = json.loads(open(f"{Const.ROOT_DIR}/data/cache", "r").read())
    for star in STARS:
        cache_file = set_simbad_values(star, cache_file)

    # Dump cache file
    with open(f"{Const.ROOT_DIR}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)
    cache_file = json.loads(open(f"{Const.ROOT_DIR}/data/cache", "r").read())

    set_img_txt(STARS)
    # Iterate through the ephemeries to add information
    for body in tqdm(EPHEMERIES_BODIES):
        cache_file = get_ephemeries_info(
            body,
            cache_file
        )

    # Dump cache file
    with open(f"{Const.ROOT_DIR}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)

    visible_messier = dict()
    for m_obj in MESSIER_OBJECTS.keys():
        Logger.log(
            "Gathering zen, altitude, and " +
            f"azimuth for {m_obj}..."
        )
        zen, altitude, azimuth = get_visible(
            m_obj,
            3.0
        )
        if '' not in (zen, altitude, azimuth):
            Logger.log(f"Sucessfully gathered data for {m_obj}!\n")
            visible = {str(m_obj): MESSIER_OBJECTS[m_obj]}
            visible[m_obj]['Zenith'] = str(zen)
            visible[m_obj]['Altitude'] = str(altitude)
            visible[m_obj]['Azimuth'] = str(azimuth)
            visible[m_obj].pop("Coordinates", None)
            visible_messier.update(visible)
            # visible_messier = {
            #     k: v for k, v in visible_messier.items() if v != ''
            # }
    visible_caldwell = dict()
    for c_obj in CALDWELL_OBJECTS.keys():
        Logger.log(
            "Gathering zen, altitude, and " +
            f"azimuth for {c_obj}..."
        )
        zen, altitude, azimuth = get_visible(
            c_obj,
            3.0
        )
        if '' not in (zen, altitude, azimuth):
            Logger.log(f"Sucessfully gathered data for {c_obj}!\n")
            visible = {str(c_obj): CALDWELL_OBJECTS[c_obj]}
            visible[c_obj]['Zenith'] = str(zen)
            visible[c_obj]['Altitude'] = str(altitude)
            visible[c_obj]['Azimuth'] = str(azimuth)
            visible[c_obj].pop("Coordinates", None)
            visible_caldwell.update(visible)
            # visible_caldwell = {
            #     k: v for k, v in visible_caldwell.items() if v != ''
            # }
    set_img_txt(visible_messier)
    set_img_txt(visible_caldwell)

    s_list = list()
    for star, data in cache_file.items():
        for key, value in data.items():
            try:
                if str(key) != "Image":
                    visible_objs[star]["Brightness"] = cache_file[star]["Brightness"]
                    visible_objs[star]["Constellation"] = cache_file[star]["Constellation"]
                    visible_objs[star]["Distance"] = f'{cache_file[star]["Distance"]} Pm'
                    visible_objs[star]["Type"] = cache_file[star]["Type"]
            except KeyError:
                continue

    for key, value in visible_objs.items():
        s_list.append({key: value})

    m_list = list()
    for key, value in visible_messier.items():
        m_list.append({key: value})

    c_list = list()
    for key, value in visible_caldwell.items():
        c_list.append({key: value})
    write_out(s_list, code=0, filename='Stars')
    write_out(m_list, code=0, filename='VisibleMessier')
    write_out(c_list, code=0, filename='VisibleCaldwell')


def set_simbad_values(celestial_obj: str, cache_file: dict) -> dict:
    """
    Call the simbad module and get the star's properties.

    :param celestial_obj: Object to get values for.
    :param cache_file: Opened cache file to apply changes to.
    :return: Cache file with added simbad values.
    """
    cache_file[celestial_obj]["Brightness"] = get_brightness(celestial_obj)

    cache_file[celestial_obj]["Constellation"] = get_constellation(
        celestial_obj
    )

    ra_dec = get_ra_dec(celestial_obj)
    cache_file[celestial_obj]["Coordinates"] = {
        "ra": ra_dec[0],
        "dec": ra_dec[1]
    }
    distance = get_distance(celestial_obj)
    cache_file[celestial_obj]["Distance"] = distance
    return cache_file


def query_jpl_horizons(ephemeries_objs: list) -> tuple:
    """
    Run ephemeries_query in as many threads as specified.

    :param ephemeries_objs: List of objects to retrieve data for.
    """
    with ThreadPoolExecutor(max_workers=Const.THREADS) as executor:
        results = executor.map(ephemeries_query, ephemeries_objs)

    unknown_objs = list()
    known_objs = list()
    for result in results:
        ephemeris, celestial_obj = result
        if ephemeris is not None:
            known_objs.append(ephemeris)
        else:
            unknown_objs.append(celestial_obj)
    ephemerides = dict()
    for obj in known_objs:
        ephemerides.update(obj)
    return (unknown_objs, ephemerides)


def invoke_skyview(stars: list) -> None:
    """
    Run skyview in as many threads as specified.

    :param stars: List of string of the stars download witrh skyview.
    """
    with ThreadPoolExecutor(max_workers=Const.THREADS) as executor:
        executor.map(get_skyview_img, stars)


def set_img_txt(celestial_objs: list) -> None:
    """
    Set the text on the image of the object.

    :param celestial_objs: List of strings of the objects to overlay text on.
    """
    with ThreadPoolExecutor(max_workers=Const.THREADS) as executor:
        executor.map(overlay_text, celestial_objs)


def get_visible(
        object_name: str,
        secz_max=3.0
) -> tuple:
    """
    Check to see if the given object is
    visible at a location in a certain time.
    :param start_time: Astropy.time object starting time range.
    :param end_time: Astropy.time object ending time range.
    :param location: Astroplan.observer object as your location.
    :param celestial_objs: List of objects to check.
    :return: Tuple of visible objects.
    """

    try:
        celestial_obj = FixedTarget.from_name(object_name)
        zen, altitude, azimuth = is_object_visible(
            celestial_obj=celestial_obj,
            secz_max=secz_max
        )
        return (zen, altitude, azimuth)
    except astropy.coordinates.name_resolve.NameResolveError as e:
        Logger.log(
            "Unable to gather name, start_altaz.alt, and " +
            f"start_altaz.az for {object_name}!\n", 40
        )
        return '', '', ''
    except TypeError as e:
        Logger.log(
            "Unable to gather name, start_altaz.alt, and " +
            f"start_altaz.az for {object_name}!\n", 40
        )
        return '', '', ''


def gen_moon_data():
    Logger.log("Retreiving data for tonight's moon...")
    today = datetime.now().strftime("%Y-%m-%d")
    illumination, phase = query()
    Logger.log("Data for tonight's moon:")
    Logger.log(f"Illumination: {illumination}\tPhase: {phase}")
    Logger.log(f"Writing data to `{Const.SLIDESHOW_DIR}/PySkySlideshow/`...")
    write_out(
        celestial_objs=[
            {
                'Moon': {
                    'Date': str(today),
                    'Illumination': illumination,
                    'Phase': phase
                }
            }
        ],
        filename=f'moon_{str(today)}'
    )
    Logger.log("Wrote file!")


def write_out(celestial_objs: list, code=0, filename=None):
    if code == 0:
        to_html_list(celestial_objs, filename=filename)
