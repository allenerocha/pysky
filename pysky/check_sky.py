"""This module is used to see if an object is visible."""
import astropy.units as u
import numpy as np
from astroplan import Observer
from astropy.coordinates import EarthLocation
from astropy.time import Time

from .const import Const
from .logger import Logger


def is_object_visible(celestial_obj, secz_max=4.1) -> tuple:
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
    location = Observer(
        location=EarthLocation.from_geodetic(
            Const.LATITUDE * u.deg, Const.LONGITUDE * u.deg, Const.ELEVATION * u.m
        ),
        name="location",
        timezone="US/Central",
    )
    start_time = Time(
        f"{Const.START_YEAR}-"
        + f"{Const.START_MONTH}-"
        + f"{Const.START_DAY} "
        + f"{Const.START_TIME}",
        format="iso",
    )
    end_time = Time(
        f"{Const.END_YEAR}-"
        + f"{Const.END_MONTH}-"
        + f"{Const.END_DAY} "
        + f"{Const.END_TIME}",
        format="iso",
    )
    Logger.log(f"Checking sec(z) for {celestial_obj.name}.")
    start_secz = location.altaz(start_time, celestial_obj).secz
    end_secz = location.altaz(end_time, celestial_obj).secz
    start_altaz = location.altaz(start_time, celestial_obj)
    end_altaz = location.altaz(end_time, celestial_obj)

    try:
        if 0 < start_secz < secz_max:
            Logger.log(
                f"Found starting sec(z) = {start_secz} for {celestial_obj.name}."
            )
            Logger.log(
                f"Zenith={start_altaz.zen} "
                + f"Altitiude={start_altaz.alt}"
                + f"Azimuth={start_altaz.az}"
            )
            # return (start_altaz.alt, start_altaz.az, end_altaz.alt, end_altaz.az)
            start_alt = start_altaz.alt
            start_az = start_altaz.az
        else:
            start_alt = "-"
            start_az = "-"
        if 0 < end_secz < secz_max:
            Logger.log(f"Found ending sec(z) = {end_secz} for {celestial_obj.name}.")
            Logger.log(
                f"Zenith={start_altaz.zen} "
                + f"Altitiude={start_altaz.alt}"
                + f"Azimuth={start_altaz.az}"
            )
            end_alt = end_altaz.alt
            end_az = end_altaz.az
        else:
            end_alt = "-"
            end_az = "-"
        return (start_alt, start_az, end_alt, end_az)
    except ValueError as e:
        Logger.log(f"Could not find sec(z) for {celestial_obj.name}.", 40)
        Logger.log(str(e), 40)
        Logger.log(start_secz, 40)
        return "-", "-", "-", "-"
    return "-", "-", "-", "-"
