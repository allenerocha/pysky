"""Get astropy information of ephemeries."""
import time

import astropy.coordinates
import astropy.time
import astropy.units
from tqdm import tqdm

from .const import Const
from .logger import Logger


def get_bodies(args: list):
    """
    Check the passed values if they are in the solar system ephemeries.
    :param args: List of arguements to check.
    :return: List of bodies or False if there are none
    """

    celestial_objs = args

    if len(celestial_objs) > 0:
        bodies = []
        # Iterate through the passed bodies
        for celestial_obj in tqdm(celestial_objs):
            try:
                # Checks if the current body is in the tuple
                EPH_BODIES = astropy.coordinates.solar_system_ephemeris.bodies
                if celestial_obj in EPH_BODIES:
                    # Adds body to the list
                    bodies.append(celestial_obj)
            except TypeError as type_err:
                Logger.log(
                    f"Error parsing object {celestial_obj}.\n\n" +
                    f"{str(type_err)}",
                    50
                )
    # Returns the list of bodies in the tuples
        return bodies
    # No bodies found in the passed list
    return False


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

        # retrives the inforamtion of the body
        Logger.log(f"Retreiving coordinates for {celestial_obj}")
        t1 = time.time()
        with astropy.coordinates.solar_system_ephemeris.set("builtin"):
            body_coordinates = astropy.coordinates.get_body(
                f"{celestial_obj}",
                astropy.time.Time(
                    f'{Const.START_YEAR}-' +
                    f'{Const.START_MONTH}-' +
                    f'{Const.START_DAY} ' +
                    f'{Const.START_TIME}',
                    format='iso'
                ),
                static_location,
            )

        Logger.log(
            f"Retreived coordinates for {celestial_obj} in {time.time() - t1}!"
        )
        return (
            body_coordinates.ra.degree,
            body_coordinates.dec.degree,
            )

    except Exception as e:
        Logger.log(str(e), 50)


def get_ephemeries_info(body: str, cache_file: dict) -> dict:
    """
    Retrieve the ephemeries information.
    :param body: Object to check.
    :param atime: astropy.time object.
    :param cache_file: Cache file.
    :return: Dictionary of the object.
    """
    Logger.log(
        f"Retreiving coordinates for {body}..."
    )
    ra, dec = get_info(body)
    cache_file[f"{body}"] = {}
    cache_file[f"{body}"]["Type"] = "planet"
    cache_file[f"{body}"]["Created"] = time.strftime(
        "%Y-%d-%m %H:%M", time.gmtime()
    )
    Logger.log(
        f"Coordinates for {body} retreived."
    )
    Logger.log(
        f"Writing coordinates for {body} to cache..."
    )
    try:
        cache_file[f"{body}"]["Coordinates"] = {  # Right acension
            "ra": ra,
            "dec": dec
        }
    except TypeError:
        print(body)
    Logger.log(
        f"Successfully wrote coordinates for {body} to cache!"
    )
    return cache_file
