"""This module parses the MessierCatalog.json and CaldwellCatalog.json and return them as dictionaries"""
import json
import os
from pathlib import Path
from .const import Const


def parse_messier(root_dir: str) -> dict:
    """
    This function parses VisibleMessierCatalog.json and returns the json object as dictionary

    :param root_dir: Root directory of this application
    :return: A Python dictionary of the MessierCatalogue.json
    """
    if not isinstance(root_dir, str):
        root_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    messier_path = Path(root_dir, "data", "MessierCatalogue.json")
    messier_file = json.loads(open(messier_path, "r").read())
    return messier_file


def check_messier(celestial_obj):
    """
    Check the messier catalog if the passed object is a member.
    :param celestial_obj: Object to check in the messier catalog.
    :return: The object if it exists
    """
    messier_catalog = parse_messier(Const.ROOT_DIR)
    if celestial_obj in messier_catalog:
        return True
    return False


def parse_caldwell(root_dir: str) -> dict:
    """
    This function parses CaldwellCatalogue.json and returns the
    json object as dictionary
    :param root_dir: Root directory of this application
    :return: A Python dictionary of the CaldwellCatalogue.json
    """
    if not isinstance(root_dir, str):
        root_dir = Path(os.path.dirname(os.path.realpath((__file__))))
    caldwell_path = Path(root_dir, "data", "CaldwellCatalogue.json")
    caldwell_file = json.loads(open(caldwell_path, "r").read())
    return caldwell_file


def check_caldwell(celestial_obj):
    """
    Check the caldwell catalogue if the passed object is a member.
    :param celestial_obj: Object to check in the caldwell catalouge.
    :return: The object if it exists
    """
    caldwell_catalog = parse_caldwell(Const.ROOT_DIR)
    if celestial_obj in caldwell_catalog:
        return True
    return False
