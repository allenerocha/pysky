"""This module retrieves the image from the passed star """

import json
import base64
import os
import urllib.request
import requests
import bs4
import utils.simbad


def get_img(celestial_obj: str, width: int, height: int, image_size: float, b_scale: str) -> object:
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

    brightness = utils.simbad.get_brightness(celestial_obj)

    # the image in in cache
    if check_cache(celestial_obj, width, height, image_size, b_scale):
        cache_file = json.loads(open("cache/data", "r").read())
        return
    # the image is not in cache

    endpoint = f'https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl?Position={celestial_obj}' \
               f'&coordinates=J2000&coordinates=&projection=Tan&pixels={width}%2C{height}' \
               f'&size={image_size}&float=on&scaling={b_scale}&resolver=SIMBAD-NED&' \
               f'Sampler=_skip_&Deedger=_skip_&rotation=&Smooth=&' \
               f'lut=colortables%2Fb-w-linear.bin&PlotColor=&grid=_skip_&gridlabels=1&' \
               f'catalogurl=&CatalogIDs=on&RGB=1&' \
               f'survey=Mellinger+Red&survey=Mellinger+Green&survey=Mellinger+Blue&' \
               f'IOSmooth=&contour=&contourSmooth=&ebins=null'
    try:
        image_request = requests.get(endpoint).text
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException("Error searching for object.")
    img_url = "https://skyview.gsfc.nasa.gov/" + \
              bs4.BeautifulSoup(image_request, features="html.parser").find('td', attrs={
                  "colspan": 3, "align": "left"
              }).find('a', href=True)['href'].replace("../", "")
    urllib.request.urlretrieve(img_url, "cache/temp.jpg")
    img_bytes = base64.b64encode(open("cache/temp.jpg", "rb").read())
    cache_file = json.loads(open("cache/data", "r").read())
    cache_file[celestial_obj] = {
        "brightness": brightness,
        "image": {
            "width": width,
            "height": height,
            "resolution": image_size,
            "brightness scaling": b_scale,
            "base64": str(img_bytes)
        }
    }
    with open("cache/data", "w") as json_out:
        json.dump(cache_file, json_out)
        img_bytes = open("cache/temp.jpg", "rb").read()
        os.remove("cache/temp.jpg")


def check_cache(celestial_obj: str, width: int, height: int,
                image_size: float, b_scale: str) -> bool:
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
    cache_file = json.loads(open("cache/data", "r").read())
    if (celestial_obj in cache_file) and\
            (cache_file[celestial_obj]["image"]["width"] == width) and\
            (cache_file[celestial_obj]["image"]["height"] == height) and\
            (cache_file[celestial_obj]["image"]["resolution"] == image_size) and\
            (cache_file[celestial_obj]["image"]["brightness scaling"] == b_scale):
        return True

    cache_file.pop(celestial_obj, None)
    return False
