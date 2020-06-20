"""Module to query JPL Horizons database."""
from astroquery.jplhorizons import Horizons
from .const import Const
import json
from .logger import Logger


def ephemeries_query(celestial_obj: str) -> tuple:
    """
    Query the table of the celestial object in a time range.

    :param celestial_obj:
    :param start:
    :param end:
    :return:
    :useage: object_query('venus', '2020-01-01', '18:00', '2020-01-02', '1:00')
    """
    cache_file = json.loads(
        open(
            f"{Const.ROOT_DIR}/data/jplcodes.json",
            "r"
        ).read())
    try:
        obj_code = cache_file[celestial_obj.lower()]
    except KeyError:
        Logger.log('Key not found in pre-defined JPL code dictionary.', 50)
        Logger.log(f'Removing {celestial_obj} from queue.', 50)
        return (None, celestial_obj)
    except Exception as e:
        Logger.log('Encountered an unknown error.', 50)
        Logger.log(f'{str(e)}', 50)
        Logger.log(f'Removing {celestial_obj} from queue.', 50)
        return (None, celestial_obj)
    try:
        location = {'lon': -87.8791, 'lat': 42.6499, 'elevation': 0.204}
        startdate = Const.START_TIME.split(' ')[0]
        starttime = Const.START_TIME.split(' ')[1]
        enddate = Const.END_TIME.split(' ')[0]
        endtime = Const.END_TIME.split(' ')[1]
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
        Logger.log('Error with key raised by JPL Horizons.', 50)
        Logger.log(f'Removing {celestial_obj} from queue.')
        return (None, celestial_obj)
    except Exception as e:
        Logger.log('Unknown error raised by JPL Horizons.', 50)
        Logger.log(f'{str(e)}', 50)
        Logger.log(f'Removing {celestial_obj} from queue.', 50)
        return (None, celestial_obj)
    eph = obj.ephemerides()['datetime_str', 'RA', 'DEC', 'V', 'delta']
    time_ra_dec = dict()
    if len(eph["RA"]) == len(eph["DEC"]):
        time_ra_dec[celestial_obj] = dict()
        for index in range(len(eph["RA"])):
            row_time = eph['datetime_str'][index]
            row_ra = eph['RA'][index]
            row_dec = eph['DEC'][index]
            row_mag = eph['V'][index]
            row_delta = eph['delta'][index]
            time_ra_dec[celestial_obj][row_time] = {
                'ra': row_ra,
                'dec': row_dec,
                'brightness': row_mag,
                'delta': row_delta * 0.000149597870691
            }
    return (time_ra_dec, None)

