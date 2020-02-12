"""This module retrieves basic data from simbad based
on which itentifier is passed via the command line
End-point http://simbad.u-strasbg.fr/simbad/sim-basic?Ident={URL}&submit=SIMBAD+search """
import sys

import bs4
import requests


def get_brightness(celestial_obj: str) -> float:
    """
    This function makes a request to the simbad website to retrieve a brightness
    :param celestial_obj: name celestial object to retreieve the brightness of
    :return: the brightness of the passed celestial object
    """
    endpoint = f"http://simbad.u-strasbg.fr/simbad/sim-basic?Ident={celestial_obj}&submit=SIMBAD+search"

    simbad_request = requests.get(endpoint)

    soup = bs4.BeautifulSoup(simbad_request.text, features="html.parser")
    table = soup.find("table", attrs={"width": "100%", "cellspacing": 2, "cellpadding": None})
    brightness = 0.0

    # iterate through the rows
    try:
        for rows in table.find_all("tr"):
            # iterate through the columns
            for cols in rows.find_all("tt"):
                if "V      " in cols.text:
                    brightness = float(cols.text.split()[1])
                    break
        return brightness
    except AttributeError:
        print(f"Error parsing the data for {celestial_obj}")
        sys.exit()
