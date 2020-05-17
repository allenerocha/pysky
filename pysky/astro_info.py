import time
from .logger import Logger

import astropy.coordinates
import astropy.time
import astropy.units
from tqdm import tqdm


def get_bodies(args: list):
    """
    Check the passed values if they are in the solar system ephemeries.
    :*args: List of arguements to check
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
            except TypeError as e:
                Logger.log(
                    f"Error parsing object {celestial_obj}.\n\n{str(e)}",
                    50
                )
        # Returns the list of bodies in the tuples
        return bodies
    # No bodies found in the passed list
    return False


def get_info(atime: str, celestial_obj: str) -> list:
    """
    This function uses the astropy module to retrieve
    distance information from the passed celestial object
    :celestial_obj: Name of the celestial object
    :return:
            [
                "hour",
                "minute",
                "second",
                "degree",
                "radian",
                "x",
                "y",
                "z",
            ]
    """

    # Type checking
    if not isinstance(celestial_obj, str):
        raise TypeError(f"{type(celestial_obj)} is not of type str.")

    try:
        static_location = astropy.coordinates.EarthLocation.from_geodetic(
            -87.8791 * astropy.units.deg,
            42.6499 * astropy.units.deg,
            height=204 * astropy.units.m,
        )

        # retrives the inforamtion of the body
        Logger.log(f"Retreiving coordinates for {celestial_obj}")
        t1 = time.time()
        with astropy.coordinates.solar_system_ephemeris.set("builtin"):
            body_coordinates = astropy.coordinates.get_body(
                f"{celestial_obj}",
                astropy.time.Time(atime),
                static_location,
            )

        Logger.log(
            f"Retreived coordinates for {celestial_obj} in {time.time() - t1}!"
        )
        return [
            body_coordinates.ra.hms[0],
            body_coordinates.ra.hms[1],
            body_coordinates.ra.hms[2],
            body_coordinates.dec.degree,
            body_coordinates.dec.radian,
            body_coordinates.cartesian.x,
            body_coordinates.cartesian.y,
            body_coordinates.cartesian.z,
        ]

    except Exception as e:
        print("aaaaaaaaaa")
        Logger.log(str(e), 50)


def get_ephemeries_info(body: str, atime: str, cache_file: dict) -> dict:
    Logger.log(
        f"Retreiving coordinates for {body}..."
    )
    COORDS = get_info(atime, body)
    cache_file[f"{body}"] = {}
    cache_file[f"{body}"]["type"] = "planet"
    cache_file[f"{body}"]["created"] = time.strftime(
        "%Y-%d-%m %H:%M", time.gmtime()
    )
    Logger.log(
        f"Coordinates for {body} retreived."
    )
    Logger.log(
        f"Writing coordinates for {body} to cache..."
    )
    try:
        cache_file[f"{body}"]["coordinates"] = {  # Right acension
            "ra": [str(COORDS[0]), str(COORDS[1]), str(COORDS[2])],
            "dec": str(COORDS[3]),
            "cartesian": [str(COORDS[5]), str(COORDS[6]), str(COORDS[7])],
        }
    except TypeError:
        print(body)
    Logger.log(
        f"Successfully wrote coordinates for {body} to cache!"
    )
    return cache_file
