"""This module parses the VisibleMessierCatalog.json and
VisibleCadwellCatalog.json and return them as dictionaries"""
import json
import os
from pathlib import Path


def parse_messier(root_dir: str) -> dict:
    """
    This function parses VisibleMessierCatalog.json and returns the
    json object as dictionary
    :param root_dir: Root directory of this application
    :return: A Python dictionary of the VisibleMessierCatalog.json
    """
    if not isinstance(root_dir, str):
        root_dir = Path(os.path.dirname(os.path.realpath((__file__))))
    messier_file = json.loads(
        open(f"{root_dir}/data/VisibleMessierCatalog.json", "r").read()
    )
    return messier_file


def check_messier(celestial_obj):
    """
    Check the messier catalog if the passed object is a member.
    :param celestial_obj: Object to check in the messier catalog.
    :return: The object if it exists
    """
    messier_catalog = parse_messier(None)
    for key, _ in messier_catalog.items():
        if key == celestial_obj:
            return messier_catalog[key]["Apparent magnitude"]
    return None


def parse_caldwell(root_dir: str) -> dict:
    """
    This function parses VisibleCaldwellCatalogue.json and returns the
    json object as dictionary
    :param root_dir: Root directory of this application
    :return: A Python dictionary of the VisibleCaldwellCatalogue.json
    """
    if not isinstance(root_dir, str):
        root_dir = Path(os.path.dirname(os.path.realpath((__file__))))
    caldwell_file = json.loads(
        open(f"{root_dir}/data/VisibleCaldwellCatalogue.json", "r").read()
    )
    return caldwell_file


def check_caldwell(celestial_obj):
    """
    Check the caldwell catalogue if the passed object is a member.
    :param celestial_obj: Object to check in the caldwell catalouge.
    :return: The object if it exists
    """
    caldwell_catalog = parse_caldwell(None)["NGC number"]
    for key, _ in caldwell_catalog.items():
        if key == celestial_obj:
            return caldwell_catalog[key]["Magnitude"]
    return None
