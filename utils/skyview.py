"""This module retrieves the image from the passed star """

import json
import PIL
import PIL.Image
import io
import base64
import requests
import bs4
import urllib.request
import os


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
    # the image in in cache
    if check_cache(celestial_obj, width, height, image_size, b_scale):
        cache_file = json.loads(open("/home/allen/PycharmProjects/PySky/cache/data", "r").read())
        imgBytes = base64.b64decode(cache_file["andromeda"]["image"]["base64"])
        img = PIL.Image.open(io.BytesIO(imgBytes))
        img.show()
        return PIL.Image.open(io.BytesIO(imgBytes))
    # the image is not in cache
    else:
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
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException("Error searching for object.")
        img_url = "https://skyview.gsfc.nasa.gov/" +\
                  bs4.BeautifulSoup(image_request, features="html.parser").find('td', attrs=
                  {"colspan": 3, "align": "left"}).find('a', href=True)['href'].replace("../", "")
        urllib.request.urlretrieve(img_url, "../cache/temp.jpg")
        cache_file = json.loads(open("../cache/data", "r").read())
        cache_file[celestial_obj] = {
            "brightness": 0,
            "image": {
                "width": width,
                "height": height,
                "resolution": image_size,
                "brightness scaling": b_scale,
                "base64": str(base64.b64encode(open("../cache/temp.jpg", "rb").read()))
            }
        }
        with open("/home/allen/PycharmProjects/PySky/cache/data", "w") as json_out:
            json.dump(cache_file, json_out)
            img = PIL.Image.open("../cache/temp.jpg")
            img.show()
            os.remove("/home/allen/PycharmProjects/PySky/cache/temp.jpg")


def check_cache(celestial_obj: str, width: int, height: int, image_size: float, b_scale:str) -> bool:
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
    cache_file = json.loads(open("/home/allen/PycharmProjects/PySky/cache/data", "r").read())
    if celestial_obj in cache_file:
        if (cache_file[celestial_obj]["image"]["width"] == width) and\
                (cache_file[celestial_obj]["image"]["height"] == height) and\
                (cache_file[celestial_obj]["image"]["resolution"] == image_size) and\
                (cache_file[celestial_obj]["image"]["brightness scaling"] == b_scale):
            return True
    else:
        cache_file.pop(celestial_obj, None)
        return False

get_img(celestial_obj="polaris", width=1920, height=1080, image_size=3.0, b_scale="Linear")

