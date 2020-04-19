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
    messier_catalog = parse_messier(None)
    for key, value in messier_catalog.items():
        if key == celestial_obj:
            return messier_catalog[key]["Apparent magnitude"]
    return None


def parse_cadwell(root_dir: str) -> dict:
    """
    This function parses VisibleCadwellCatalog.json and returns the
    json object as dictionary
    :param root_dir: Root directory of this application
    :return: A Python dictionary of the VisibleCadwellCatalog.json
    """
    if not isinstance(root_dir, str):
        root_dir = Path(os.path.dirname(os.path.realpath((__file__))))
    cadwell_file = json.loads(
        open(f"{root_dir}/data/VisibleCadwellCatalog.json", "r").read()
    )
    return cadwell_file


def check_cadwell(celestial_obj):
    cadwell_catalog = parse_cadwell(None)["NGC number"]
    for key, value in cadwell_catalog.items():
        if key == celestial_obj:
            return cadwell_catalog[key]["Magnitude"]
    return None
