"""Module to query JPL Horizons database."""
import json

from astroquery.jplhorizons import Horizons

from .const import Const
from .logger import Logger


def ephemeries_query(celestial_obj: str) -> tuple:
    """
    Query the table of the celestial object in a time range.

    :param celestial_obj:
    :return:
    :useage: object_query('venus', '2020-01-01', '18:00', '2020-01-02', '1:00')
    """
    jplcodes = json.loads(
        open(
            f"{Const.ROOT_DIR}/data/jplcodes.json",
            "r"
        ).read())
    try:
        obj_code = jplcodes[celestial_obj.lower()]
    except KeyError:
        Logger.log('Key not found in pre-defined JPL code dictionary.', 40)
        Logger.log(f'Removing {celestial_obj} from queue.', 40)
        return (None, celestial_obj)
    except ValueError as e:
        Logger.log('Encountered an value error.', 40)
        Logger.log(f'{str(e)}', 50)
        Logger.log(f'Removing {celestial_obj} from queue.', 40)
        return (None, celestial_obj)

    except Exception as e:
        Logger.log('Encountered an unknown error.', 40)
        Logger.log(f'{str(e)}', 50)
        Logger.log(f'Removing {celestial_obj} from queue.', 40)
        return (None, celestial_obj)
    try:
        location = {
            'lon': Const.LONGITUDE,
            'lat': Const.LATITUDE,
            'elevation': (Const.ELEVATION / 1000.0)
        }
        startdate = f'{Const.START_YEAR}-{Const.START_MONTH}-{Const.START_DAY}'
        starttime = Const.START_TIME
        enddate = f'{Const.END_YEAR}-{Const.END_MONTH}-{Const.END_DAY}'
        endtime = Const.END_TIME
        obj = Horizons(
            id=obj_code,
            location=location,
            epochs={
                'start': f'{startdate} {starttime}',
                'stop': f'{enddate} {endtime}',
                'step': '1m'
            },
            id_type='id'
        )
    except KeyError:
        Logger.log('Error with key raised by JPL Horizons.', 40)
        Logger.log(f'Removing {celestial_obj} from queue.')
        return (None, celestial_obj)
    except ValueError as e:
        Logger.log('Encountered an value error.', 40)
        Logger.log(f'{str(e)}', 50)
        Logger.log(f'Removing {celestial_obj} from queue.', 40)
        return (None, celestial_obj)
    except Exception as e:
        Logger.log('Unknown error raised by JPL Horizons.', 40)
        Logger.log(f'{str(e)}', 40)
        Logger.log(f'Removing {celestial_obj} from queue.', 40)
        return (None, celestial_obj)

    eph = obj.ephemerides()[
        'datetime_str',
        'RA',
        'DEC',
        'V',
        'delta',
        'illumination'
    ]

    time_ra_dec = dict()
    if len(eph["RA"]) == len(eph["DEC"]):
        time_ra_dec[celestial_obj] = dict()
        for index in range(len(eph["RA"])):
            row_time = eph['datetime_str'][index]
            row_ra = eph['RA'][index]
            row_dec = eph['DEC'][index]
            row_mag = eph['V'][index]
            row_delta = eph['delta'][index]
            row_illumination = eph['illumination'][index]
            time_ra_dec[celestial_obj][row_time] = {
                'ra': row_ra,
                'dec': row_dec,
                'Brightness': row_mag,
                'Delta': row_delta * 0.000149597870691,
                'Illumination': row_illumination
            }
    return (time_ra_dec, None)
