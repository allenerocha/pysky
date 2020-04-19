"""This module retrieves the image from the passed star """

import base64
import io
import json
import logging
import os
import sys
import time
import urllib.request
from logging import critical, error, info
from pathlib import Path

import bs4
import PIL.Image
import requests

from .catalog_parse import check_cadwell, check_messier
from .image_manipulation import overlay_text
from .simbad import get_brightness, get_constellation, get_ra_dec


def get_skyview_img(
    celestial_obj: str,
    width: int,
    height: int,
    image_size: float,
    b_scale: str,
    root_dir: str,
) -> int:
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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    BRIGHTNESS_THREASHOLD = 4.5

    # the image in in cache
    info(f"Checking if image of {celestial_obj} is cached...")
    if check_cache(celestial_obj, width, height, image_size, b_scale, root_dir):
        return

    brightness = get_brightness(celestial_obj, root_dir)
    if brightness is None:
        critical(f"Error searching for {celestial_obj} in the cadwell and messier catalogs.")
            return 2

    constellation = get_constellation(celestial_obj, root_dir)
    ra_dec = get_ra_dec(celestial_obj, root_dir)

    if brightness > BRIGHTNESS_THREASHOLD:
        return 1

    info("Establishing connection to skyview server...")
    t1 = time.time()
    if (
        urllib.request.urlopen(
            "https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl"
        ).getcode()
        != 200
    ):
        critical(
            "Error trying to connect to the skyview server taking {time.time() - t1}."
        )
        sys.exit()
    info(f"Connection to skyview server successful taking {time.time() - t1} seconds!")

    endpoint = (
        f"https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl?Position={celestial_obj}"
        f"&coordinates=J2000&coordinates=&projection=Tan&pixels={width}%2C{height}"
        f"&size={image_size}&float=on&scaling={b_scale}&resolver=SIMBAD-NED&"
        f"Sampler=_skip_&Deedger=_skip_&rotation=&Smooth=&"
        f"lut=colortables%2Fb-w-linear.bin&PlotColor=&grid=_skip_&gridlabels=1&"
        f"catalogurl=&CatalogIDs=on&RGB=1&"
        f"survey=Mellinger+Red&survey=Mellinger+Green&survey=Mellinger+Blue&"
        f"IOSmooth=&contour=&contourSmooth=&ebins=null"
    )
    try:
        t1 = time.time()
        info(f"Downloading webpage for {celestial_obj}...")
        image_request = requests.get(endpoint).text
    except requests.exceptions.RequestException as e:
        critical(f"{str(e)}")
        critical("Error searching for object.")
        return 2
    info(f"Downloaded successfully in {time.time() - t1} seconds!")

    info("Parsing webpage...")
    try:
        img_url = "https://skyview.gsfc.nasa.gov/" + bs4.BeautifulSoup(
            image_request, features="html.parser"
        ).find("td", attrs={"colspan": 3, "align": "left"}).find("a", href=True)[
            "href"
        ].replace(
            "../", ""
        )
        info("Webpage parsed!")
    except AttributeError as e:
        critical(
            f"Error trying to parse the web page of {celestial_obj}!\n\n{str(e)}\n"
        )
        return 3

    info(f"Downloading image of {celestial_obj}...")
    t1 = time.time()
    urllib.request.urlretrieve(img_url, f"{root_dir}/data/temp.jpg")
    img_bytes = base64.b64encode(open(f"{root_dir}/data/temp.jpg", "rb").read())
    info(f"Downloaded successfully in {time.time() - t1} seconds!")

    info(f"Writing {celestial_obj} data to cache...")
    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())
    try:
        cache_file[celestial_obj] = {
            "type": "star",
            "constellation": f"{constellation}",
            "created": time.strftime("%Y-%d-%m %H:%M", time.gmtime()),
            "brightness": brightness,
            "coordinates": {"ra": ra_dec[0], "dec": ra_dec[1]},
            "image": {
                "width": width,
                "height": height,
                "resolution": image_size,
                "brightness scaling": b_scale,
                "base64": str(img_bytes),
            },
        }
        info(f"Finished writing {celestial_obj} data to cache!")

        info("Saving changes to cache...")
        with open(f"{root_dir}/data/cache", "w") as json_out:
            json.dump(cache_file, json_out, indent=4, sort_keys=True)
            img_bytes = open(f"{root_dir}/data/temp.jpg", "rb").read()
            os.remove(f"{root_dir}/data/temp.jpg")
        info("Successfully saved changes to cache!")

        # decode the image from the cache file from b64 to bytes
        decoded_img = base64.b64decode(
            cache_file[celestial_obj]["image"]["base64"][1:-1]
        )
        # save the returned image containing the overlayed information
        overlay_text(
            PIL.Image.open(io.BytesIO(decoded_img)),
            [
                f"Name: {celestial_obj}",
                f"Constellation: {cache_file[celestial_obj]['constellation']}",
                f"Brightness: {cache_file[celestial_obj]['brightness']}",
            ],
            root_dir,
        )
        # Reload edited cache file
        cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())
        # Write image to disk
        img = PIL.Image.open(
            io.BytesIO(
                base64.b64decode(cache_file[celestial_obj]["image"]["base64"][1:-1])
            )
        )
        img.save(
            f"{Path.home()}/PySkySlideshow/{celestial_obj.replace(' ', '_')}-{cache_file[celestial_obj]['image']['width']}-{cache_file[celestial_obj]['image']['height']}-{cache_file[celestial_obj]['image']['resolution']}-{cache_file[celestial_obj]['image']['brightness scaling']}.png"
        )

    except TypeError as e:
        critical(str(e))
        sys.exit()
    except ConnectionResetError as e:
        critical(str(e))
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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())
    if (
        (celestial_obj in cache_file)
        and (cache_file[celestial_obj]["image"]["width"] == width)
        and (cache_file[celestial_obj]["image"]["height"] == height)
        and (cache_file[celestial_obj]["image"]["resolution"] == image_size)
        and (cache_file[celestial_obj]["image"]["brightness scaling"] == b_scale)
    ):
        files = [
            f
            for f in os.listdir(f"{Path.home()}/PySkySlideshow")
            if os.path.isfile(f"{Path.home()}/PySkySlideshow/{f}")
        ]
        if len(files) < 1:
            return False

        elif (
            f"{Path.home()}/PySkySlideshow/{celestial_obj}-{width}-{height}-{image_size}-{b_scale}.png"
            not in files
        ):
            cache_file.pop(celestial_obj, None)
            return False

        info(files)
        info(f"Image of {celestial_obj} is cached.\n")
        return True

    else:
        cache_file.pop(celestial_obj, None)
        error(f"Image of {celestial_obj} not cached.\nPreparing to download...")
    return False
