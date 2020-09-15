"""Contains functions related to the moon."""

import json
import re

import bs4
import requests

from .const import Const


def query() -> tuple:
    """
    Get the illumination and phase of the moon for today.
    :return: illumination and phase
    """
    ENDPOINT = (
            "https://www.moongiant.com/phase/"
            + f"{Const.START_MONTH}/{Const.START_DAY}/{Const.START_YEAR}"
    )
    tags = re.compile(r"<\\*/*[A-Za-z]*>|\\n")
    response = requests.get(ENDPOINT).text
    soup = bs4.BeautifulSoup(response, features="html.parser")
    soup.prettify()
    text = soup.text.split("var jArray=")[1].split(";")[0]
    data = json.loads(tags.sub("", text))

    for item in data["2"]:
        if "illumination" in item.lower():
            illumination = item.replace("Illumination: ", "")

        elif "phase" in item.lower():
            phase = item.replace("Phase: ", "")
    return illumination, phase
