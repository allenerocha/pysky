"""This module retrieves basic data from simbad based on which itentifier is passed via the command line"""
import json
import re
import sys
from pathlib import Path

import astroquery.simbad
import requests
from bs4 import BeautifulSoup

from .const import Const
from .logger import Logger


def get_classification(celestial_obj: str) -> str:
    """
    Scrape the simbad website to get the object's classification.

    :param celestial_obj: name celestial object to retrieve the brightness of.
    :return: the brightness of the passed celestial object.
    """
    Logger.log(f"Retrieving classification for {celestial_obj}...")
    regex = re.compile(r"\s*\r?\n")
    endpoint = f"http://simbad.u-strasbg.fr/simbad/sim-basic?Ident={celestial_obj}&submit=SIMBAD+search"
    web_data = requests.get(endpoint).text
    soup = BeautifulSoup(web_data, "html.parser")
    classification = soup.find("td", attrs={"id": "basic_data"}).find("font").text
    if classification is not None:
        Logger.log(f"Found classification for {celestial_obj}!")
        classification = re.sub(regex, "", classification)
        regex = re.compile(r"\(.*\)")
        classification = re.sub(regex, "", classification)
        return classification.split("--")[-1].strip()
    Logger.log(f"Could not find classification for {celestial_obj}!", 30)
    return "-"


def get_brightness(celestial_obj: str) -> float:
    """
    Make a request to the simbad website to retrieve a brightness.

    :param celestial_obj: name celestial object to retrieve the brightness of.
    :return: the brightness of the passed celestial object.
    """

    Logger.log(f"Retrieving brightness for {celestial_obj}...")

    astroquery.simbad.Simbad.reset_votable_fields()
    try:
        # Add brightness column
        astroquery.simbad.Simbad.add_votable_fields("flux(V)")

        # Remove the other columns
        astroquery.simbad.Simbad.remove_votable_fields("main_id")
        astroquery.simbad.Simbad.remove_votable_fields("coordinates")

        # Check result for "--"
        if str(astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0]) == "--":
            Logger.log(f"Could not find brightness for {celestial_obj}!", 30)
            celestial_obj_aux = celestial_obj + "_A"
            Logger.log(f"Attempting to find brightness for {celestial_obj_aux}!", 30)
            BRIGHTNESS_FIELD = str(
                astroquery.simbad.Simbad.query_object(celestial_obj_aux)[0][0]
            )
            brightness = float(BRIGHTNESS_FIELD)

        else:
            BRIGHTNESS_FIELD = str(
                astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0]
            )
            brightness = float(BRIGHTNESS_FIELD)
        # Return brightness
        Logger.log(f"Retrieved brightness for {celestial_obj}!\n")
        return brightness

    # Occurs when the object is not in SIMBADS's database
    except TypeError as type_err:
        Logger.log(
            f"Error parsing the data for {celestial_obj}. "
            + f"Simbad only contains info on stars.\n\n{str(type_err)}",
            50,
        )

        try:
            Logger.log(f"Could not find brightness for {celestial_obj_aux}!", 30)
            Logger.log(
                f"Attempting to find brightness for {celestial_obj} using it's IUE!",
                30,
            )
            Logger.log("Resetting votable fields")
            astroquery.simbad.Simbad.reset_votable_fields()
            astroquery.simbad.Simbad.add_votable_fields("iue")
            astroquery.simbad.Simbad.remove_votable_fields("main_id")
            astroquery.simbad.Simbad.remove_votable_fields("coordinates")
            NEW_OBJECT_FIELD = (
                str(astroquery.simbad.Simbad.query_object(celestial_obj)[0][0])
                .replace("b", "")
                .replace("'", "")
            )

            astroquery.simbad.Simbad.reset_votable_fields()
            # Add brightness column
            astroquery.simbad.Simbad.add_votable_fields("flux(V)")

            # Remove the other columns
            astroquery.simbad.Simbad.remove_votable_fields("main_id")
            astroquery.simbad.Simbad.remove_votable_fields("coordinates")

            BRIGHTNESS_FIELD = str(
                astroquery.simbad.Simbad.query_object(NEW_OBJECT_FIELD)[0][0]
            )

            brightness = float(BRIGHTNESS_FIELD)

            return brightness

        except TypeError as type_err:
            Logger.log(
                f"Error parsing the data for {celestial_obj}. "
                + f"Simbad only contains info on stars.\n\n{str(type_err)}",
                50,
            )
            return None

    # Occurs for multiple stars
    except ValueError as value_err:
        Logger.log(
            f"Error converting brightness for {celestial_obj}. "
            + "Simbad does not contain brightnesses for double or "
            + f"multiple stars.\n\n{str(value_err)}",
            50,
        )

        return None


def get_constellation(celestial_obj: str) -> str:
    """
    This function returns the TLA of the constellation from the passed object.
    :param celestial_obj: name celestial object to retrieve the TLA.
    :return: TLA of the constellation.
    """
    astroquery.simbad.Simbad.reset_votable_fields()
    Logger.log(f"Retrieving constellation for {celestial_obj}...")
    const_abbrvs = json.loads(
        open(Path(Const.ROOT_DIR, "data", "ConstellAbbrevs.json"), "r").read()
    )
    try:
        astroquery.simbad.Simbad.remove_votable_fields("coordinates")
        constellation = str(
            astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0]
        ).split()[-1][:-1]
        Logger.log(f"Retrieved constellation abbreviation for {celestial_obj}!\n")
        try:
            constellation = const_abbrvs[str(constellation).lower()]
        except KeyError as e:
            Logger.log(
                f"{constellation} not found in constellation abbreviation dictionary",
                50,
            )
            Logger.log(str(e), 50)
        return constellation

    # Occurs when the object is not in SIMBAS's database
    except TypeError as type_err:
        Logger.log(
            f"Error parsing the data for {celestial_obj}. "
            + f"Simbad only contains info on stars.\n\n{str(type_err)}",
            50,
        )
        sys.exit()

    # Occurs for multiple stars
    except ValueError as value_err:
        Logger.log(
            f"Error converting constellation for {celestial_obj}."
            + f"\n\n{str(value_err)}",
            50,
        )
        sys.exit()


def get_ra_dec(celestial_obj: str) -> list:
    """
    This function uses simbad to retrieve the right ascension
    and declination from the object passed as an argument.
    :param celestial_obj: name of the celestial
                          object to retrieve the ra and dec.
    :return: List of the right ascension and declination.
    """
    astroquery.simbad.Simbad.reset_votable_fields()
    astroquery.simbad.Simbad.remove_votable_fields("main_id")
    Logger.log(f"Retrieving right ascension and declination for {celestial_obj}...")
    ras = astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0].split()
    try:
        ra = [int(float(r)) for r in ras]
    except ValueError as value_err:
        Logger.log(f"{value_err}", 50)
        exit()
    decs = astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][1].split()
    dec = [int(float(d)) for d in decs]
    ra_dec = [ra, dec]
    Logger.log(f"Retrieved ra and dec for {celestial_obj}!\n")
    return ra_dec


def get_distance(celestial_obj: str) -> float:
    """
    Calculate the distance in Pm.
    :param celestial_obj: Object to query simbad.
    :return: Distance of the object in Pm.
    """
    astroquery.simbad.Simbad.reset_votable_fields()
    astroquery.simbad.Simbad.add_votable_fields("parallax")
    astroquery.simbad.Simbad.remove_votable_fields("main_id")
    astroquery.simbad.Simbad.remove_votable_fields("coordinates")
    Logger.log(f"Retrieving distance for {celestial_obj}...")
    parsec_dist = astroquery.simbad.Simbad.query_object(celestial_obj)[0][0]

    if parsec_dist is None:
        return None

    return int(float(parsec_dist) * 30.86)
