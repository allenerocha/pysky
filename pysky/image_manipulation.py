"""This module will be used to overlay information of the
celestial body over image of the celestial body using PIL"""
import base64
import json
import logging
import os
from logging import info

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


def overlay_text(img: object, overlay_text: list, root_dir: str) -> object:
    """
    This adds text to the image
    :img: Image file to overlay the text
    :overlay_text: List of text to overlay on the image
    :return: None
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    # only save the height of the image
    _, img_h = img.size

    cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())
    info(f"Overlaying text to image...")
    overlayed = PIL.ImageDraw.Draw(img, mode="RGBA")
    overlayed.multiline_text(
        xy=(10, int(img_h * 0.8)),  # xy of the location for the text to  be overlayed
        text="\n".join(overlay_text),  # concats all passed strings in the list
        fill=(255, 255, 255, 100),  # white text with alpha=100
        # stroke_width=1,  # thickness of the stroke
        # stroke_fill=(0, 0, 0, 100),  # black stroke with alpha=100
        spacing=1,  # in between each new line
        align="left",
    )

    info("Adding edited image to cache file...")
    img.save(fp=f"{root_dir}/data/temp.png", format="PNG")
    img_bytes = base64.b64encode(open(f"{root_dir}/data/temp.png", "rb").read())
    celestial_obj = overlay_text[0].replace("Name: ", "")
    # write the edited image to the cache file
    cache_file[celestial_obj]["image"]["base64"] = str(img_bytes)[1:]
    info("Edited image added to cache file!")

    with open(f"{root_dir}/data/cache", "w") as json_out:
        info("Saving edited cache file...")
        json.dump(cache_file, json_out)
        os.remove(f"{root_dir}/data/temp.png")
        info("Edited cache file saved!")
