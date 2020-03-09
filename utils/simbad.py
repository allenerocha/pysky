"""This module retrieves basic data from simbad based
on which itentifier is passed via the command line"""
import sys
import astroquery.simbad

def get_brightness(celestial_obj: str) -> float:
    """
    This function makes a request to the simbad website to retrieve a brightness
    :param celestial_obj: name celestial object to retreieve the brightness of
    :return: the brightness of the passed celestial object
    """

    #view all possible fields => astroquery.list_votable_fields()

    try:
        astroquery.simbad.Simbad.add_votable_fields("flux(V)")
        astroquery.simbad.Simbad.remove_votable_fields("main_id")
        astroquery.simbad.Simbad.remove_votable_fields("coordinates")

        brightness = float(str(astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0]))
        return brightness
    except TypeError as e:
        print(f"Error parsing the data for {celestial_obj}. Simbad only contains info on stars.\n\n{str(e)}")
        sys.exit()
    except ValueError as e:
        print(f"Error converting brightness for {celestial_obj}. Simbad does not contain brightnesses for double or multiple stars.\n\n{str(e)}")
        sys.exit()

