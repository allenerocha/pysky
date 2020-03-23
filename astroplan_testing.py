"""This module is used to see if an object is visible"""
import astroplan
import astropy
import astropy.units


def is_object_visible(celestial_obj: object, start_time: object, end_time: object, location: object, secz_max=2.0) -> tuple:
    """
    :param celestial_obj: object to view (astropy.coordinates.SkyCoord())
    :param start_time: starting range for the viewing time (astropy.time.Time())
    :param end_time: ending range for the viewing time (astropy.time.Time())
    :param secz_max:
    :param location: location of viewing site (astropy.coordinates.EarthLocation())
    :return: tuple if the object is up or not during the time range given (string, alt, az || '', '', '')
    """

    start_secz = location.altaz(start_time, celestial_obj).secz
    end_secz = location.altaz(end_time, celestial_obj).secz
    start_altaz = location.altaz(start_time, celestial_obj)

    if start_secz < 2.0 or end_secz < 2.0:
        return celestial_obj.name, start_altaz.alt, start_altaz.az
    return '', '', ''

