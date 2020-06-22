"""This module is used to see if an object is visible."""
from .logger import Logger
from astroplan import Observer
import numpy as np


def is_object_visible(
        celestial_obj,
        start_time,
        end_time,
        location,
        secz_max
) -> tuple:
    """
    :param celestial_obj: object to view (astropy.coordinates.SkyCoord())
    :param start_time:  starting range for the
                        viewing time (astropy.time.Time())
    :param end_time: ending range for the viewing time (astropy.time.Time())
    :param secz_max:
    :param location: location of viewing site
                     (astropy.coordinates.EarthLocation())
    :return: tuple if the object is up or not during
             the time range given (string, alt, az || '', '', '')
    """
    Logger.log(f"Checking sec(z) for {celestial_obj}.")
    start_secz = location.altaz(start_time, celestial_obj).secz
    end_secz = location.altaz(end_time, celestial_obj).secz
    start_altaz = location.altaz(start_time, celestial_obj)

    try:
        if np.all(start_secz < secz_max) or np.all(end_secz < secz_max):
            Logger.log(f"Found sec(z) for {celestial_obj.name}.")
            return start_altaz.zen, start_altaz.alt, start_altaz.az
    except ValueError:
        Logger.log(f"Could not find ound sec(z) for {celestial_obj.name}.")
        return '', '', ''
