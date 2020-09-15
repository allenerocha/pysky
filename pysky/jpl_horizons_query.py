"""Module to query JPL Horizons database."""
import json
from statistics import median
from pathlib import Path

from astroquery.jplhorizons import Horizons

from .const import Const
from .logger import Logger


def ephemeris_query(celestial_obj: str) -> tuple:
    """
    Query the table of the celestial object in a time range.

    :param celestial_obj:
    :return:
    :usage: object_query('venus', '2020-01-01', '18:00', '2020-01-02', '1:00')
    """
    jplcodes = json.loads(
        open(Path(Const.ROOT_DIR, "data", "jplcodes.json"), "r").read()
    )
    try:
        obj_code = jplcodes[celestial_obj.lower()]
    except KeyError:
        Logger.log("Key not found in pre-defined JPL code dictionary.", 40)
        Logger.log(f"Removing {celestial_obj} from queue.", 40)
        return None, celestial_obj
    except ValueError as e:
        Logger.log("Encountered an value error.", 40)
        Logger.log(f"{str(e)}", 50)
        Logger.log(f"Removing {celestial_obj} from queue.", 40)
        return None, celestial_obj

    except Exception as e:
        Logger.log("Encountered an unknown error.", 40)
        Logger.log(f"{str(e)}", 50)
        Logger.log(f"Removing {celestial_obj} from queue.", 40)
        return None, celestial_obj
    try:
        location = {
            "lon": Const.LONGITUDE,
            "lat": Const.LATITUDE,
            "elevation": (Const.ELEVATION / 1000.0),
        }
        startdate = f"{Const.START_YEAR}-{Const.START_MONTH}-{Const.START_DAY}"
        starttime = Const.START_TIME
        enddate = f"{Const.END_YEAR}-{Const.END_MONTH}-{Const.END_DAY}"
        endtime = Const.END_TIME
        obj = Horizons(
            id=obj_code,
            location=location,
            epochs={
                "start": f"{startdate} {starttime}",
                "stop": f"{enddate} {endtime}",
                "step": "15m",
            },
            id_type="id",
        )
    except KeyError:
        Logger.log("Error with key raised by JPL Horizons.", 40)
        Logger.log(f"Removing {celestial_obj} from queue.")
        return None, celestial_obj
    except ValueError as e:
        Logger.log("Encountered an value error.", 40)
        Logger.log(f"{str(e)}", 50)
        Logger.log(f"Removing {celestial_obj} from queue.", 40)
        return None, celestial_obj
    except Exception as e:
        Logger.log("Unknown error raised by JPL Horizons.", 40)
        Logger.log(f"{str(e)}", 40)
        Logger.log(f"Removing {celestial_obj} from queue.", 40)
        return None, celestial_obj

    eph = obj.ephemerides()[
        "datetime_str",
        "RA",
        "DEC",
        "AZ",
        "EL",
        "V",
        "delta",
        "illumination",
        "constellation",
    ]
    const_abbrvs = json.loads(
        open(Path(Const.ROOT_DIR, "data", "ConstellAbbrevs.json"), "r").read()
    )
    time_ra_dec = dict()
    time_ra_dec[celestial_obj] = dict()
    mag_list = list()
    distance_list = list()
    for index in range(len(eph["datetime_str"])):
        if index == 0:
            ra = eph["RA"][index]
            dec = eph["DEC"][index]
            time_ra_dec[celestial_obj]["Coordinates"] = {"ra": ra, "dec": dec}
        row_time = eph["datetime_str"][index]
        row_az = eph["AZ"][index]
        row_alt = eph["EL"][index]
        row_mag = eph["V"][index]
        mag_list.append(row_mag)
        row_delta = float(eph["delta"][index])
        row_delta = row_delta * 0.000149597870691
        distance_list.append(row_delta)
        row_constellation = const_abbrvs[str(eph["constellation"][index]).lower()]
        row_illumination = eph["illumination"][index]
        time_ra_dec[celestial_obj]["Constellation"] = row_constellation
        time_ra_dec[celestial_obj][row_time] = {
            "az": row_az,
            "alt": row_alt,
            "Brightness": row_mag,
            "Distance": row_delta,
            "Illumination": row_illumination,
        }

    time_ra_dec[celestial_obj]["Brightness"] = round(median(mag_list), 1)
    time_ra_dec[celestial_obj]["Distance"] = round(median(distance_list), 8)

    with open(
        Path(
            Const.SLIDESHOW_DIR,
            "PySkySlideshow",
            f"{celestial_obj}-{startdate}-{starttime.replace(':', '')}-{enddate}-{endtime.replace(':', '')}-data.json",
        ),
        "w",
    ) as json_out:
        json.dump(time_ra_dec[celestial_obj], json_out, indent=4)
    return time_ra_dec, None
