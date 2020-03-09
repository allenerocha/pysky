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

    astroquery.simbad.Simbad.reset_votable_fields()
    try:
        # Add brightness column
        astroquery.simbad.Simbad.add_votable_fields("flux(V)")

        # Remove the other columns
        astroquery.simbad.Simbad.remove_votable_fields("main_id")
        astroquery.simbad.Simbad.remove_votable_fields("coordinates")

        # Convert brightness to float
        brightness = float(str(astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0]))

        # Return brightness
        return brightness

    # Occurs when the object is not in SIMBAS's database
    except TypeError as e:
        print(f"Error parsing the data for {celestial_obj}. Simbad only contains info on stars.\n\n{str(e)}")
        sys.exit()

    # Occurs for multiple stars
    except ValueError as e:
        print(f"Error converting brightness for {celestial_obj}. Simbad does not contain brightnesses for double or multiple stars.\n\n{str(e)}")
        sys.exit()


def get_constellation(celestial_obj: str) -> str:
    """
    This function returns the TLA of the constellation from the passed object
    :param celestial_obj: name celestial object to retreieve the TLA
    :return: TLA of the constellation
    """
    astroquery.simbad.Simbad.reset_votable_fields()
    try:
        astroquery.simbad.Simbad.remove_votable_fields("coordinates")
        constellation = str(astroquery.simbad.Simbad.query_object(f"{celestial_obj}")[0][0]).split()[-1][:-1]
        return constellation

    # Occurs when the object is not in SIMBAS's database
    except TypeError as e:
        print(f"Error parsing the data for {celestial_obj}. Simbad only contains info on stars.\n\n{str(e)}")
        sys.exit()

    # Occurs for multiple stars
    except ValueError as e:
        print(f"Error converting constellation for {celestial_obj}.\n\n{str(e)}")
        sys.exit()


