import time
import astropy.time
import astropy.coordinates


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

    if type(celestial_obj) != type(str()):
        raise TypeError(f"{type(celestial_obj)} is not of type str.")

    try:
        static_location = astropy.coordinates.EarthLocation.of_site('greenwich')
        t1 = time.strftime("%Y-%d-%m %H:%M", time.gmtime())
        with astropy.coordinates.solar_system_ephemeris.set('builtin'):
            # this assignment creates warings
            # WARNING: failed to download https://maia.usno.navy.mil/ser7/finals2000A.all and https://toshi.nofs.navy.mil/ser7/finals2000A.all
            # WARNING: Tried to get polar motions for times after IERS data is valid.
            # WARNING: failed to download https://maia.usno.navy.mil/ser7/finals2000A.all and https://toshi.nofs.navy.mil/ser7/finals2000A.all
            # WARNING: (some) times are outside of range covered by IERS table.
            # WARNING: failed to download https://maia.usno.navy.mil/ser7/finals2000A.all and https://toshi.nofs.navy.mil/ser7/finals2000A.all

            body_coordinates = astropy.coordinates.get_body(
                                                    f'{celestial_obj}',
                                                    astropy.time.Time(t1),
                                                    static_location
                                                )

        return [body_coordinates.ra.hms[0], body_coordinates.ra.hms[1], body_coordinates.ra.hms[2], body_coordinates.dec.degree, body_coordinates.dec.radian, body_coordinates.cartesian.x, body_coordinates.cartesian.y, body_coordinates.cartesian.z]

    except Exception as e:
        print(str(e))

