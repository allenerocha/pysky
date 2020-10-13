"""This module retrieves the image from the passed star """

import sys
import time
import urllib.request
from pathlib import Path
import os
import bs4
import requests

from .const import Const
from .logger import Logger


def get_skyview_img(celestial_obj: str) -> int:
    """
    This module retrieves the image from the skyview endpoint
    if it not already cached. After retrieval, it will cache the image.
    :param celestial_obj: Name of object to download.
    :return: Integer code.
    """
    width, height = (1080, 1080)
    image_size = 3.5
    b_scale = "Linear"
    # the image in in cache
    Logger.log("Establishing connection to skyview server...")
    t1 = time.time()
    if (
        urllib.request.urlopen(
            "https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl"
        ).getcode()
        != 200
    ):
        Logger.log(
            "Error trying to connect to the skyview server "
            + f"taking {time.time() - t1}.",
            50,
        )
        sys.exit()
    Logger.log(
        "Connection to skyview server "
        + f"successful taking {time.time() - t1} seconds!"
    )

    endpoint = (
        "https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl?"
        + f"Position={celestial_obj.replace(' ', '%20')}"
        "&coordinates=J2000&coordinates=&projection=Tan&" + f"pixels={width}%2C{height}"
        f"&size={image_size}&float=on&scaling={b_scale}&resolver=SIMBAD-NED&"
        "Sampler=_skip_&Deedger=_skip_&rotation=&Smooth=&"
        "lut=colortables%2Fb-w-linear.bin&PlotColor=&grid=_skip_"
        + "&gridlabels=1&catalogurl=&CatalogIDs=on&RGB=1&"
        "survey=Mellinger+Red&survey=Mellinger+Green&survey=Mellinger+Blue&"
        "IOSmooth=&contour=&contourSmooth=&ebins=null"
    )
    Logger.log(endpoint)
    try:
        t1 = time.time()
        Logger.log(f"Downloading webpage for {celestial_obj}...")
        image_request = requests.get(endpoint).text
    except requests.exceptions.RequestException as req_except:
        Logger.log(f"{str(req_except)}", 50)
        Logger.log("Error searching for object.", 50)
        return 2
    Logger.log(f"Downloaded successfully in {time.time() - t1} seconds!")

    Logger.log("Parsing webpage...")
    try:
        img_url = "https://skyview.gsfc.nasa.gov/" + bs4.BeautifulSoup(
            image_request, features="html.parser"
        ).find("td", attrs={"colspan": 3, "align": "left"}).find("a", href=True)[
            "href"
        ].replace(
            "../", ""
        )
        Logger.log("Webpage parsed!")
    except AttributeError as attrib_except:
        Logger.log(
            "Error trying to parse the web page of "
            + f"{celestial_obj}!\n\n{str(attrib_except)}\n",
            50,
        )
        return 3

    Logger.log(f"Downloading image of {celestial_obj}...")
    t1 = time.time()
    if not os.path.isdir(Path(Const.SLIDESHOW_DIR, "PySkySlideshow", "garbage")):
        os.makedirs(Path(Const.SLIDESHOW_DIR, "PySkySlideshow", "garbage"))
    urllib.request.urlretrieve(
        img_url,
        Path(
            Const.SLIDESHOW_DIR,
            "PySkySlideshow",
            "garbage",
            f"{celestial_obj}.temp.jpg",
        ),
    )
    Logger.log(f"Downloaded successfully in {time.time() - t1} seconds!")
