"""Main module that calls all relevant modules."""
import json
import os.path
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import warnings

from datetime import datetime
from .argument_parser import cli_parse
from .astro_info import get_ephemeries_info
from .catalog_parse import parse_caldwell, parse_messier
from .check_sky import is_object_visible
from .image_manipulation import overlay_text
from .prefs import check_integrity, read_user_prefs
from .skyview import get_skyview_img
from .logger import Logger
from .const import Const
from .simbad import get_brightness, get_constellation
from .simbad import get_ra_dec, get_distance
from .output import to_html_list
from .moonquery import query
from .jpl_horizons_query import ephemeries_query

import astropy
from astropy.coordinates import SkyCoord

# Set up the thing to catch the warning (and potentially others)
with warnings.catch_warnings(record=True) as w:
    # import the modules
    import astroplan
    from astroplan import OldEarthOrientationDataWarning

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

from tqdm import tqdm

def invoke():
    """
    Call all other relevant functions.
    """

    cli_parse()

    START_TIME = Const.START_TIME
    END_TIME = Const.END_TIME

    check_integrity()

    CALDWELL_OBJECTS = parse_caldwell(Const.ROOT_DIR)
    MESSIER_OBJECTS = parse_messier(Const.ROOT_DIR)
    USER_OBJECTS = read_user_prefs()

    gen_moon_data()

    LOCATION = astroplan.Observer(
        location=astropy.coordinates.EarthLocation.from_geodetic(
            Const.LATITUDE * astropy.units.deg,
            Const.LONGITUDE * astropy.units.deg,
            height=(Const.ELEVATION/1000.0) * astropy.units.m,
        ),
        name="Location",
    )

    STARS, EPHEMERIES = query_jpl_horizons(USER_OBJECTS)

    EPHEMERIES_BODIES = list(EPHEMERIES.keys())


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
            START_TIME,
            cache_file
        )

    # Dump cache file
    with open(f"{Const.ROOT_DIR}/data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)

    visible_objs = dict()
    for objs in cache_file.keys():
        Logger.log(
            "Gathering zen, altitude, and " +
            f"azimuth for {objs}..."
        )
        try:
            zen, altitude, azimuth = get_visible(
                START_TIME,
                END_TIME,
                LOCATION,
                5.0,
                cache_file[objs]['Coordinates']['ra'],
                cache_file[objs]['Coordinates']['dec']
            )
        except KeyError:
            print(cache_file[objs])
#            exit()
        if '' not in (zen, altitude, azimuth):
            Logger.log(f"Sucessfully gathered data for {objs}!\n")
            visible = {str(objs): cache_file[objs]}
            visible[objs].pop('Image', None)
            visible[objs]['Zenith'] = zen
            visible[objs]['Altitude'] = altitude
            visible[objs]['Azimuth'] = azimuth
            visible_objs.update(visible)
            
    visible_messier = dict()
    for m_obj in MESSIER_OBJECTS.keys():
        Logger.log(
            "Gathering zen, altitude, and " +
            f"azimuth for {m_obj}..."
        )
    
        zen, altitude, azimuth = get_visible(
            START_TIME,
            END_TIME,
            LOCATION,
            2.0,
            MESSIER_OBJECTS[m_obj]['Coordinates']['ra'],
            MESSIER_OBJECTS[m_obj]['Coordinates']['dec']
        )
        if '' not in (zen, altitude, azimuth):
            Logger.log(f"Sucessfully gathered data for {m_obj}!\n")
            visible = {str(m_obj): MESSIER_OBJECTS[m_obj]}
            visible[m_obj]['Zenith'] = zen
            visible[m_obj]['Altitude'] = altitude
            visible[m_obj]['Azimuth'] = azimuth
            visible_messier.update(visible)
            
    visible_caldwell = dict()
    for c_obj in CALDWELL_OBJECTS.keys():
        Logger.log(
            "Gathering zen, altitude, and " +
            f"azimuth for {c_obj}..."
        )
    
        zen, altitude, azimuth = get_visible(
            START_TIME,
            END_TIME,
            LOCATION,
            2.0,
            CALDWELL_OBJECTS[c_obj]['Coordinates']['ra'],
            CALDWELL_OBJECTS[c_obj]['Coordinates']['dec']
        )
        if '' not in (zen, altitude, azimuth):
            Logger.log(f"Sucessfully gathered data for {c_obj}!\n")
            visible = {str(c_obj): CALDWELL_OBJECTS[c_obj]}
            visible[c_obj]['Zenith'] = zen
            visible[c_obj]['Altitude'] = altitude
            visible[c_obj]['Azimuth'] = azimuth
            visible_caldwell.update(visible)
            
    set_img_txt(visible_messier)
    
    set_img_txt(visible_caldwell)

    # write_out(mclist, code=0, filename='VisibleMessier')
    
    # write_out(cclist, code=0, filename='VisibleCaldwell')
    



def set_simbad_values(celestial_obj: str, cache_file: dict) -> dict:
    """
    Call the simbad module and get the brightness, constellation,
    and location.
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
    :param :
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
    start_time,
    end_time,
    location,
    secz_max,
    ra,
    dec
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
    
    celestial_obj = SkyCoord(ra, dec, frame="icrs", unit="deg")
    
    
    try:
        zen, altitude, azimuth = is_object_visible(
            celestial_obj=celestial_obj,
            start_time=start_time,
            end_time=end_time,
            location=location,
            secz_max=secz_max
        )
        return (zen, altitude, azimuth)
    except astropy.coordinates.name_resolve.NameResolveError as e:
        Logger.log(
            "Unable to gather name, start_altaz.alt, and " +
            f"start_altaz.az for ra={ra} dec={dec}!\n", 40
        )
        return '', '', ''
    except TypeError as e:
        Logger.log(
            "Unable to gather name, start_altaz.alt, and " +
            f"start_altaz.az for ra={ra} dec={dec}!\n", 40
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
                'name': 'Moon',
                'date': str(today),
                'illumination': illumination,
                'phase': phase
            }
        ],
        filename='moon'
    )
    Logger.log("Wrote file!")


def write_out(celestial_objs: list, code=0, filename=None):
    if code == 0:
        to_html_list(celestial_objs, filename=filename)
