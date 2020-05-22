"""This module will be used to overlay information of the
celestial body over image of the celestial body using PIL"""
import base64
import json
import os
import io
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from .logger import Logger
from .catalog_parse import check_messier, check_caldwell
from .catalog_parse import parse_messier, parse_caldwell
from .const import Const
PIL.Image.MAX_IMAGE_PIXELS = 933120000


def overlay_text(celestial_obj: str) -> None:
    """
    This adds text to the image
    :img: Image file to overlay the text
    :overlay_text: List of text to overlay on the image
    """

    cache_file = json.loads(
        open(
            f"{Const.ROOT_DIR}/data/cache",
            "r"
        )
        .read()
    )
    overlay_txt = list()

    if check_messier(celestial_obj):
        m_catalog = parse_messier(Const.ROOT_DIR)
        static_data_path = f"{Const.ROOT_DIR}/data/static_data/"
        img = PIL.Image.open(
            f"{static_data_path}{celestial_obj.replace(' ', '')}.jpg"
        )
        if m_catalog[celestial_obj]['Common name'] != "":
            overlay_txt.append(
                "Common Name: " +
                f"{m_catalog[celestial_obj]['Common name']}"
            )
            overlay_txt.append(f"Catalogue Name: {celestial_obj}")
            overlay_txt.append(
                "Constellation: " +
                f"{m_catalog[celestial_obj]['Constellation']}"
            )
            overlay_txt.append(
                "Brightness: " +
                f"{m_catalog[celestial_obj]['Apparent magnitude']}"
            )
            overlay_txt.append(
                "Distance (petameters): " +
                f"{m_catalog[celestial_obj]['Distance (petameters)']} Pm"
            )
        img = add_text(img, overlay_txt)
        img.save(
            fp=f"{Const.SLIDESHOW_DIR}/PySkySlideshow/" +
            f"{celestial_obj.replace(' ', '')}.png",
            format="PNG"
        )

    elif check_caldwell(celestial_obj):
        c_catalogue = parse_caldwell(Const.ROOT_DIR)
        static_data_path = f"{Const.ROOT_DIR}/data/static_data/"
        img = PIL.Image.open(
            f"{static_data_path}{celestial_obj.replace(' ', '')}.jpg"
        )
        if c_catalogue['NGC number'][celestial_obj]['Common name'] != "":
            overlay_txt.append(
                "Common Name: " +
                f"{c_catalogue['NGC number'][celestial_obj]['Common name']}",
            )
        overlay_txt.append(f"Catalogue Name: {celestial_obj}")
        overlay_txt.append(
            "Constellation: " +
            f"{c_catalogue['NGC number'][celestial_obj]['Constellation']}"
            )
        overlay_txt.append(
            "Brightness: " +
            f"{c_catalogue['NGC number'][celestial_obj]['Magnitude']}"
            )
        overlay_txt.append(
            "Distance (petameters): " +
            f"{c_catalogue['NGC number'][celestial_obj]['Distance (petameters)']} Pm"
            )
        img = add_text(img, overlay_txt)
        img.save(
            fp=f"{Const.SLIDESHOW_DIR}/PySkySlideshow/" +
            f"{celestial_obj.replace(' ', '')}.png",
            format="PNG"
        )

    else:
        decoded_img = base64.b64decode(
            cache_file[celestial_obj]["image"]["base64"][1:-1]
        )
        img = PIL.Image.open(io.BytesIO(decoded_img))
        overlay_txt = [
            f"Name: {celestial_obj}",
            f"Constellation: {cache_file[celestial_obj]['constellation']}",
            f"Brightness: {cache_file[celestial_obj]['brightness']}",
        ]
        img = add_text(img, overlay_txt)
        Logger.log(f"Adding edited image of {celestial_obj} to cache file...")
        img.save(
            fp=f"{Const.ROOT_DIR}/data/{celestial_obj}.temp.png", format="PNG"
        )

        with open(f"{Const.ROOT_DIR}/data/cache", "w") as json_out:
            Logger.log("Saving edited cache file...")
            json.dump(cache_file, json_out)
            os.remove(f"{Const.ROOT_DIR}/data/{celestial_obj}.temp.png")
            Logger.log("Edited cache file saved!")
            img.save(
                f"{Const.SLIDESHOW_DIR}/PySkySlideshow/" +
                f"{celestial_obj.replace(' ', '_')}-" +
                f"{cache_file[celestial_obj]['image']['width']}-" +
                f"{cache_file[celestial_obj]['image']['height']}-" +
                f"{cache_file[celestial_obj]['image']['resolution']}-" +
                f"{cache_file[celestial_obj]['image']['brightness scaling']}" +
                ".png"
            )
    os.remove(f"{Const.ROOT_DIR}/data/{celestial_obj}.temp.jpg")


def add_text(img: object, overlay_txt: list) -> object:
    """
    Add the text on the image.
    :param img: PIL.Image object to overlay text on.
    :param overlay_txt: List of string to overlay on the image.
    :return: PIL.Image object with the overlayed text.
    """
    # only save the height of the image
    try:
        _, img_h = img.size
    except AttributeError:
        Logger.log(f"Error opening {img}", 50)

    Logger.log("Overlaying text to image...")
    fonts = [
        f for f in os.listdir(f"{Const.ROOT_DIR}/data/res") if ".ttf" in f
    ]

    overlayed = PIL.ImageDraw.Draw(img, mode="RGBA")
    if len(fonts) >= 1:
        fnt = PIL.ImageFont.truetype(
            f"{Const.ROOT_DIR}/data/res/{fonts[0]}",
            int(img_h/50)
        )
        overlayed.multiline_text(
            xy=(10, int(img_h * 0.8)),  # xy for the text to be overlayed
            text="\n".join(overlay_txt),  # concats all strings in the list
            fill=(255, 255, 255, 100),  # white text with alpha=100
            font=fnt,
            stroke_width=1,  # thickness of the stroke
            stroke_fill=(0, 0, 0, 100),  # black stroke with alpha=100
            spacing=1,  # in between each new line
            align="left",
        )
    else:
        overlayed.multiline_text(
            xy=(10, int(img_h * 0.8)),  # xy for the text to be overlayed
            text="\n".join(overlay_text),  # concats all strings in the list
            fill=(255, 255, 255, 100),  # white text with alpha=100
            spacing=1,  # in between each new line
            align="left",
        )

    return img
