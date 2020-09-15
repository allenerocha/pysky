"""Get astropy information of ephemeris."""
import time

import astropy.coordinates
import astropy.time
import astropy.units

from .const import Const
from .logger import Logger


def get_info(celestial_obj: str):
    """
    This function uses the astropy module to retrieve
    distance information from the passed celestial object.
    :celestial_obj: Name of the celestial object.
    :return: List of the location of the object.
    """

    # Type checking
    if not isinstance(celestial_obj, str):
        raise TypeError(f"{type(celestial_obj)} is not of type str.")

    try:
        static_location = astropy.coordinates.EarthLocation.from_geodetic(
            Const.LATITUDE * astropy.units.deg,
            Const.LONGITUDE * astropy.units.deg,
            height=(Const.ELEVATION / 1000.0) * astropy.units.m,
        )

        # Retrieves the information of the body
        Logger.log(f"Retrieving coordinates for {celestial_obj}")
        t1 = time.time()
        with astropy.coordinates.solar_system_ephemeris.set("jpl"):
            body_coordinates = astropy.coordinates.get_body(
                f"{celestial_obj}",
                astropy.time.Time(
                    f"{Const.START_YEAR}-"
                    + f"{Const.START_MONTH}-"
                    + f"{Const.START_DAY} "
                    + f"{Const.START_TIME}",
                    format="iso",
                ),
                static_location,
            )

        Logger.log(f"Retrieved coordinates for {celestial_obj} in {time.time() - t1}!")
        return (
            body_coordinates.ra.degree,
            body_coordinates.dec.degree,
        )

    except Exception as e:
        Logger.log(str(e), 50)


def get_ephemeris_info(body: str, cache_file: dict) -> dict:
    """
    Retrieve the ephemeris information from the given body and update the cache file accordingly.
    :param body: Object to check.
    :param atime: astropy.time object.
    :param cache_file: Cache file.
    :return: Dictionary of the object.
    """
    Logger.log(f"Retrieving coordinates for {body}...")
    ra_dec_tuple = get_info(body)
    if ra_dec_tuple is None:
        ra = "-"
        dec = "-"
    else:
        ra, dec = ra_dec_tuple
    # cache_file[f"{body}"] = {}
    cache_file[f"{body}"]["Type"] = "planet"
    cache_file[f"{body}"]["Created"] = time.strftime("%Y-%d-%m %H:%M", time.gmtime())
    Logger.log(f"Coordinates for {body} retrieved.")
    Logger.log(f"Writing coordinates for {body} to cache...")
    try:
        cache_file[f"{body}"]["Coordinates"] = {"ra": ra, "dec": dec}  # Right ascension
    except TypeError:
        print(body)
    Logger.log(f"Successfully wrote coordinates for {body} to cache!")
    return cache_file
