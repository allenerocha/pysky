"""This module retrieves basic data from simbad based
on which itentifier is passed via the command line"""
import logging
import sys
from logging import critical, error, info, warning

import astroquery.simbad


def get_brightness(celestial_obj: str, root_dir: str) -> float:
    """
    This function makes a request to the simbad website to retrieve a brightness
    :param celestial_obj: name celestial object to retreieve the brightness of
    :return: the brightness of the passed celestial object
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    # view all possible fields => astroquery.simbad.Simbad.list_votable_fields()

    info(f"Retrieving brightness for {celestial_obj}...")

    astroquery.simbad.Simbad.reset_votable_fields()
    try:
        # Add brightness column
        astroquery.simbad.Simbad.add_votable_fields("flux(V)")

        # Remove the other columns
        astroquery.simbad.Simbad.remove_votable_fields("main_id")
        astroquery.simbad.Simbad.remove_votable_fields("coordinates")

        # Check result for "--"
        if str(astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0]) == "--":
            celestial_obj = celestial_obj + "_A"
            brightness = float(
                str(astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0])
            )

        else:
            brightness = float(
                str(astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0])
            )
        # Return brightness
        info(f"Retrieved brightness for {celestial_obj}!\n")
        return brightness

    # Occurs when the object is not in SIMBAS's database
    except TypeError as e:
        critical(
            f"Error parsing the data for {celestial_obj}. Simbad only contains info on stars.\n\n{str(e)}"
        )
        sys.exit()

    # Occurs for multiple stars
    except ValueError as e:
        critical(
            f"Error converting brightness for {celestial_obj}. Simbad does not contain brightnesses for double or multiple stars.\n\n{str(e)}"
        )
        sys.exit()


def get_constellation(celestial_obj: str, root_dir) -> str:
    """
    This function returns the TLA of the constellation from the passed object
    :param celestial_obj: name celestial object to retreieve the TLA
    :return: TLA of the constellation
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )
    astroquery.simbad.Simbad.reset_votable_fields()
    info(f"Retrieving constellation for {celestial_obj}...")
    try:
        astroquery.simbad.Simbad.remove_votable_fields("coordinates")
        constellation = str(
            astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0]
        ).split()[-1][:-1]
        info(f"Retrieved constellation for {celestial_obj}!\n")
        return constellation

    # Occurs when the object is not in SIMBAS's database
    except TypeError as e:
        critical(
            f"Error parsing the data for {celestial_obj}. Simbad only contains info on stars.\n\n{str(e)}"
        )
        sys.exit()

    # Occurs for multiple stars
    except ValueError as e:
        critical(f"Error converting constellation for {celestial_obj}.\n\n{str(e)}")
        sys.exit()


def get_ra_dec(celestial_obj: str, root_dir: str) -> list:
    """
    This function uses simbad to retrieve the right acension
    and declination from the object passed as an argument
    :param celestial_obj: name of the celestial object to retreive the ra and dec
    :return: [ra, dec]
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )
    astroquery.simbad.Simbad.reset_votable_fields()
    astroquery.simbad.Simbad.remove_votable_fields("main_id")
    info(f"Retreiving right acension and declination for {celestial_obj}...")
    ra_dec = [
        astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0].split(),
        astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][1].split(),
    ]
    info(f"Retrieved ra and dec for {celestial_obj}!")
    return ra_dec