"""This module retrieves the image from the passed star """

import json
import base64
import time
import os
import io
import sys
import urllib.request
import PIL.Image
import requests
import bs4
import utils.simbad
import utils.image_manipulation
import utils.astro_info


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

    BRIGHTNESS_THREASHOLD = 4.5

    # the image in in cache
    print(f"Checking if image of {celestial_obj} is cached...")
    if check_cache(celestial_obj, width, height, image_size, b_scale):
        cache_file = json.loads(open("data/cache", "r").read())
        imgBytes = base64.b64decode(cache_file[f"{celestial_obj}"]["image"]["base64"])
        img = PIL.Image.open(io.BytesIO(imgBytes))
        img.show()
        return

    #a_info = utils.astro_info.get_info(celestial_obj)
    brightness = utils.simbad.get_brightness(celestial_obj)
    constellation = utils.simbad.get_constellation(celestial_obj)
    ra_dec = utils.simbad.get_ra_dec(celestial_obj)

    #if brightness > BRIGHTNESS_THREASHOLD:
    #    return None


    print("Establishing connection to skyview server...")
    t1 = time.time()
    if(urllib.request.urlopen("https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl").getcode() != 200):
        print("Error trying to connect to the skyview server taking {time.time() - t1}.")
        sys.exit()
    print(f"Connection to skyview server successful taking {time.time() - t1} seconds!")

    endpoint = f'https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl?Position={celestial_obj}' \
               f'&coordinates=J2000&coordinates=&projection=Tan&pixels={width}%2C{height}' \
               f'&size={image_size}&float=on&scaling={b_scale}&resolver=SIMBAD-NED&' \
               f'Sampler=_skip_&Deedger=_skip_&rotation=&Smooth=&' \
               f'lut=colortables%2Fb-w-linear.bin&PlotColor=&grid=_skip_&gridlabels=1&' \
               f'catalogurl=&CatalogIDs=on&RGB=1&' \
               f'survey=Mellinger+Red&survey=Mellinger+Green&survey=Mellinger+Blue&' \
               f'IOSmooth=&contour=&contourSmooth=&ebins=null'
    try:
        t1 = time.time()
        print(f"Downloading webpage for {celestial_obj}...")
        image_request = requests.get(endpoint).text
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException("Error searching for object.")
    print(f"Downloaded successfully in {time.time() - t1} seconds!")

    print("Parsing webpage...")
    img_url = "https://skyview.gsfc.nasa.gov/" + \
              bs4.BeautifulSoup(image_request, features="html.parser").find('td', attrs={
                  "colspan": 3, "align": "left"
              }).find('a', href=True)['href'].replace("../", "")
    print("Webpage parsed!")

    print(f"Downloading image of {celestial_obj}...")
    t1 = time.time()
    urllib.request.urlretrieve(img_url, "data/temp.jpg")
    img_bytes = base64.b64encode(open("data/temp.jpg", "rb").read())
    print(f"Downloaded successfully in {time.time() - t1} seconds!")

    print(f"Writing {celestial_obj} data to cache...")
    cache_file = json.loads(open("data/cache", "r").read())
    try:
        cache_file[celestial_obj] = {
            "type": "star",
            "constellation": f"{constellation}",
            "created": time.strftime("%Y-%d-%m %H:%M", time.gmtime()),
            "brightness": brightness,
            "coordinates" : {
                "ra": ra_dec[0],
                "dec": ra_dec[1]
            },
            "image": {
                "width": width,
                "height": height,
                "resolution": image_size,
                "brightness scaling": b_scale,
                "base64": str(img_bytes)
            }
        }
        print(f"Finished writing {celestial_obj} data to cache!")

        print("Saving changes to cache...")
        with open("data/cache", "w") as json_out:
            json.dump(cache_file, json_out, indent=4, sort_keys=True)
            img_bytes = open("data/temp.jpg", "rb").read()
            os.remove("data/temp.jpg")
        print("Successfully saved changes to cache!")

        # decode the image from the cache file from b64 to bytes
        decoded_img = base64.b64decode(cache_file[celestial_obj]['image']['base64'][1:-1])
        # save the returned image containing the overlayed information
        utils.image_manipulation.add_text(PIL.Image.open(io.BytesIO(decoded_img)), [f"Name: {celestial_obj}", f"Constellation: {cache_file[celestial_obj]['constellation']}", f"Brightness: {cache_file[celestial_obj]['brightness']}"])
        #Write image to disk
        img = PIL.Image.open(io.BytesIO(base64.b64decode(cache_file[celestial_obj]['image']['base64'][1:-1])))
        img.save(f"slideshow/{celestial_obj}-{cache_file[celestial_obj]['image']['width']}-{cache_file[celestial_obj]['image']['height']}-{cache_file[celestial_obj]['image']['resolution']}-{cache_file[celestial_obj]['image']['brightness scaling']}-{cache_file[celestial_obj]['created']}.png")
        # pop the image
        #cache_file

    except TypeError as e:
        print(str(e))
        sys.exit()
    except ConnectionResetError as e:
        print(str(e))
        sys.exit()


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
    cache_file = json.loads(open("data/cache", "r").read())
    if (celestial_obj in cache_file) and\
            (cache_file[celestial_obj]["image"]["width"] == width) and\
            (cache_file[celestial_obj]["image"]["height"] == height) and\
            (cache_file[celestial_obj]["image"]["resolution"] == image_size) and\
            (cache_file[celestial_obj]["image"]["brightness scaling"] == b_scale):
        print(f"Image of {celestial_obj} is cached.\n")
        return True

    else:
        cache_file.pop(celestial_obj, None)
        os.listdir
        files = [f for f in os.listdir("slideshow") if os.path.isfile(join("slideshow", f))]
        print(files)

        print(f"Image of {celestial_obj} not cached.\nPreparing to download...")
    return False

