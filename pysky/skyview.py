"""This module retrieves the image from the passed star """

import base64
import io
import json
import os
import sys
import time
import urllib.request
from .logger import Logger

import bs4
import PIL.Image
import requests

from .catalog_parse import check_caldwell, check_messier
from .image_manipulation import overlay_text
from .simbad import get_brightness, get_constellation, get_ra_dec
from .const import Const


def get_skyview_img(celestial_obj: str) -> int:
    """
    This module retrieves the image from the skyview endpoint
    if it not already cached. After retrieval, it will cache the image.
    :param celestial_obj: Name of object to view
    :param width: Width of the output picture desired
    :param height: Height of the output picture desired
    :param image_size: Degrees of the image
    :param b_scale
    :return: Bytes
    """
    width, height = (1080, 1080)
    image_size = 3.5
    b_scale = "Linear"
    root_dir = os.path.abspath(os.path.dirname(__file__))

    # the image in in cache
    Logger.log(f"Checking if image of {celestial_obj} is cached...")
    if check_cache(
        celestial_obj, width, height,
        image_size, b_scale, root_dir
    ):
        return

    Logger.log("Establishing connection to skyview server...")
    t1 = time.time()
    if (
        urllib.request.urlopen(
            "https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl"
        ).getcode()
        != 200
    ):
        Logger.log(
            "Error trying to connect to the skyview server " +
            f"taking {time.time() - t1}.",
            50
        )
        sys.exit()
    Logger.log(
        "Connection to skyview server " +
        f"successful taking {time.time() - t1} seconds!"
    )

    endpoint = (
        "https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl?" +
        f"Position={celestial_obj}"
        "&coordinates=J2000&coordinates=&projection=Tan&" +
        f"pixels={width}%2C{height}"
        f"&size={image_size}&float=on&scaling={b_scale}&resolver=SIMBAD-NED&"
        "Sampler=_skip_&Deedger=_skip_&rotation=&Smooth=&"
        "lut=colortables%2Fb-w-linear.bin&PlotColor=&grid=_skip_" +
        "&gridlabels=1&catalogurl=&CatalogIDs=on&RGB=1&"
        "survey=Mellinger+Red&survey=Mellinger+Green&survey=Mellinger+Blue&"
        "IOSmooth=&contour=&contourSmooth=&ebins=null"
    )
    try:
        t1 = time.time()
        Logger.log(f"Downloading webpage for {celestial_obj}...")
        image_request = requests.get(endpoint).text
    except requests.exceptions.RequestException as e:
        Logger.log(f"{str(e)}", 50)
        Logger.log("Error searching for object.", 50)
        return 2
    Logger.log(f"Downloaded successfully in {time.time() - t1} seconds!")

    Logger.log("Parsing webpage...")
    try:
        img_url = "https://skyview.gsfc.nasa.gov/" + bs4.BeautifulSoup(
            image_request, features="html.parser"
        ).find(
            "td",
            attrs={
                "colspan": 3,
                "align": "left"
                }
            ).find("a", href=True)["href"].replace("../", "")
        Logger.log("Webpage parsed!")
    except AttributeError as e:
        Logger.log(
            "Error trying to parse the web page of " +
            f"{celestial_obj}!\n\n{str(e)}\n",
            50
        )
        return 3

    Logger.log(f"Downloading image of {celestial_obj}...")
    t1 = time.time()
    urllib.request.urlretrieve(
        img_url,
        f"{root_dir}/data/{celestial_obj}.temp.jpg"
    )
    img_bytes = base64.b64encode(
        open(
            f"{root_dir}/data/{celestial_obj}.temp.jpg", "rb").read()
        )
    Logger.log(f"Downloaded successfully in {time.time() - t1} seconds!")

    Logger.log(f"Writing {celestial_obj} data to cache...")
    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())
    try:
        cache_file[celestial_obj] = {
            "type": "star",
            "created": time.strftime("%Y-%d-%m %H:%M", time.gmtime()),
            "image": {
                "width": width,
                "height": height,
                "resolution": image_size,
                "brightness scaling": b_scale,
                "base64": str(img_bytes),
            },
        }
        Logger.log(f"Finished writing {celestial_obj} data to cache!")

        Logger.log("Saving changes to cache...")
        with open(f"{root_dir}/data/cache", "w") as json_out:
            json.dump(cache_file, json_out, indent=4, sort_keys=True)
            img_bytes = open(
                f"{root_dir}/data/{celestial_obj}.temp.jpg",
                "rb"
            ).read()
        Logger.log("Successfully saved changes to cache!")

    except TypeError as e:
        Logger.log(str(e), 50)
        sys.exit()
    except ConnectionResetError as e:
        Logger.log(str(e), 50)
        sys.exit()
    return 4


def check_cache(
    celestial_obj: str,
    width: int,
    height: int,
    image_size: float,
    b_scale: str,
    root_dir: str,
) -> bool:
    """
    This module retrieves the image from the skyview endpoint
    if it not already cached. After retrieval, it will cache the image.
    :param celestial_obj: Name of object to view
    :param width: Width of the output picture desired
    :param height: Height of the output picture desired
    :param image_size: Degrees of the image
    :param b_scale brightness scale for image processing
    :return: boolean if depending on if the specific cache exists
    """
    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())
    try:
        if (
            (celestial_obj in cache_file)
            and (cache_file[celestial_obj]["image"]["width"] == width)
            and (cache_file[celestial_obj]["image"]["height"] == height)
            and (cache_file[celestial_obj]["image"]["resolution"] == image_size)
            and (
                cache_file[celestial_obj]["image"]["brightness scaling"] == b_scale
            )
        ):
            files = [
                f
                for f in os.listdir(f"{Const.SLIDESHOW_DIR}/PySkySlideshow")
                if os.path.isfile(f"{Const.SLIDESHOW_DIR}/PySkySlideshow/{f}")
            ]
    except KeyError:
        return False
        if len(files) < 1:
            return False

        elif (
            f"{Const.SLIDESHOW_DIR}/PySkySlideshow/{celestial_obj}-" +
            f"{width}-{height}-{image_size}-{b_scale}.png"
            not in files
        ):
            cache_file.pop(celestial_obj, None)
            return False

        Logger.log(f"Image of {celestial_obj} is cached.\n")
        return True

    else:
        cache_file.pop(celestial_obj, None)
        Logger.log(
            f"Image of {celestial_obj} not cached.\nPreparing to download...",
            30
        )
    return False
