"""Contains functions related to the moon."""

import requests
import bs4
import re
import json


def query() -> tuple:
    """
    Get the illumination and phase of the moon for today.
    :return: illumination and phase
    """
    ENDPOINT = "https://www.moongiant.com/phase/today/"
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
