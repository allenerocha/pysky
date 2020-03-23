import time
import astropy.time
import astropy.coordinates
import astropy.coordinates
import astropy.units


def get_bodies(*args) -> list:
    """
    Checks the passed values if they are in the solar system ephemeries
    :*args: List of arguements to check
    :return: List of bodies or False if there are none
    """

    celestial_objs = list(args)[0]

    if len(celestial_objs) > 0:
        bodies = []
        # Iterate through the passed bodies
        for celestial_obj in celestial_objs:
            try:
                # Checks if the current body is in the tuple
                if celestial_obj in astropy.coordinates.solar_system_ephemeris.bodies:
                    # Adds body to the list
                    bodies.append(celestial_obj)
            except TypeError as e:
                print(f'Error parsing object {celestial_obj}.\n\n{str(e)}')
        # Returns the list of bodies in the tuples
        return bodies
    # No bodies found in the passed list
    return False


def get_info(celestial_obj: str) -> list:
    """
    This function uses the astropy module to retrieve distance information from the passed celestial object
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
    if type(celestial_obj) != type(str()):
        raise TypeError(f"{type(celestial_obj)} is not of type str.")

    try:
        # 42.650167, -87.880403
        #static_location = astropy.coordinates.EarthLocation.of_site(42.650167, -87.880403)
        static_location = astropy.coordinates.EarthLocation.from_geodetic(-87.8791*astropy.units.deg, 42.6499*astropy.units.deg, height=204*astropy.units.m)

        # Current time

        # retrives the inforamtion of the body
        print(f"Retreiving coordinates for {celestial_obj}")
        t1 = time.time()
        with astropy.coordinates.solar_system_ephemeris.set('builtin'):
            body_coordinates = astropy.coordinates.get_body(
                                                    f'{celestial_obj}',
                                                    astropy.time.Time("2020-01-22 23:22"),
                                                    static_location
                                                )

        print(f"Retreived coordinates for {celestial_obj} in {time.time() - t1}!")
        return [body_coordinates.ra.hms[0], body_coordinates.ra.hms[1], body_coordinates.ra.hms[2], body_coordinates.dec.degree, body_coordinates.dec.radian, body_coordinates.cartesian.x, body_coordinates.cartesian.y, body_coordinates.cartesian.z]

    except Exception as e:
        print(str(e))

