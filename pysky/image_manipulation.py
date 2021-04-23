"""This module will be used to overlay information of the
celestial body over image of the celestial body using PIL"""
import json
import os
from pathlib import Path

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

from .catalog_parse import check_caldwell, check_messier, parse_caldwell, parse_messier
from .const import Const
from .logger import Logger

PIL.Image.MAX_IMAGE_PIXELS = 933120000


def overlay_text(celestial_obj: str, extra_data=None) -> None:
    """
    This adds text to the image
    :img: Image file to overlay the text
    :overlay_text: List of text to overlay on the image
    """
    conv_str = "1 Pm = 1 000 000 000 000 000 meters"
    cache_file = json.loads(open(Path(Const.ROOT_DIR, "data", "cache"), "r").read())
    overlay_txt = list()

    if check_messier(celestial_obj):
        Logger.log(f"Overlaying text for {celestial_obj}")
        m_catalog = parse_messier(Const.ROOT_DIR)
        static_data_path = Path(Const.ROOT_DIR, "data", "static_data")
        img = PIL.Image.open(
            Path(static_data_path, f"{celestial_obj.replace(' ', '')}.jpg")
        )
        if m_catalog[celestial_obj]["Common name"] != "":
            overlay_txt.append(
                "Common Name: " + f"{m_catalog[celestial_obj]['Common name']}"
            )
        overlay_txt.append(f"Catalogue Name: {celestial_obj}")
        overlay_txt.append("Type: " + f"{m_catalog[celestial_obj]['Type']}")
        overlay_txt.append(
            "Constellation: " + f"{m_catalog[celestial_obj]['Constellation']}"
        )
        overlay_txt.append("Brightness: " + f"{m_catalog[celestial_obj]['Brightness']}")
        overlay_txt.append(
            "Distance (petameters): " + f"{m_catalog[celestial_obj]['Distance']} Pm "
        )
        overlay_txt.append(conv_str)
        img = add_text(img, overlay_txt)
        img.save(
            fp=Path(
                Const.SLIDESHOW_DIR,
                "PySkySlideshow",
                f"{celestial_obj.replace(' ', '')}.png",
            ),
            format="PNG",
        )
        Logger.log(f"Overlaid text for {celestial_obj}")

    elif check_caldwell(celestial_obj):
        Logger.log(f"Overlaying text for {celestial_obj}")
        c_catalogue = parse_caldwell(Const.ROOT_DIR)
        Logger.log(f"Opening image for {celestial_obj}")
        static_data_path = f"{Const.ROOT_DIR}/data/static_data/"
        img = PIL.Image.open(
            Path(static_data_path, f"{celestial_obj.replace(' ', '')}.jpg")
        )
        Logger.log(f"Adding common name for {celestial_obj}")
        if c_catalogue[celestial_obj]["Common name"] != "":
            overlay_txt.append(
                "Common Name: " + f"{c_catalogue[celestial_obj]['Common name']}"
            )
        Logger.log(f"Adding catalogue name for {celestial_obj}")
        overlay_txt.append(f"Catalogue Name: {celestial_obj}")
        Logger.log(f"Adding type for {celestial_obj}")
        overlay_txt.append("Type: " + f"{c_catalogue[celestial_obj]['Type']}")
        Logger.log(f"Adding constellation for {celestial_obj}")
        overlay_txt.append(
            "Constellation: " + f"{c_catalogue[celestial_obj]['Constellation']}"
        )
        Logger.log(f"Adding brightness for {celestial_obj}")
        overlay_txt.append(
            "Brightness: " + f"{c_catalogue[celestial_obj]['Brightness']}"
        )
        Logger.log(f"Adding distance for {celestial_obj}")
        overlay_txt.append(
            "Distance (petameters): " + f"{c_catalogue[celestial_obj]['Distance']} Pm "
        )
        overlay_txt.append(conv_str)
        img = add_text(img, overlay_txt)
        img.save(
            fp=Path(
                Const.SLIDESHOW_DIR,
                "PySkySlideshow",
                f"{celestial_obj.replace(' ', '')}.png",
            ),
            format="PNG",
        )
            
    elif celestial_obj.lower() == "moon":
        Logger.log(f"Overlaying text for {celestial_obj}")
        if not os.path.isdir(Path(Const.SLIDESHOW_DIR, "PySkySlideshow", "garbage")):
            Logger.log("Garbage directory not found! Creating it.", 30)
            os.makedirs(Path(Const.SLIDESHOW_DIR, "PySkySlideshow", "garbage"))
        Logger.log("Loading image data.")
        
        static_data_path = Path(Const.ROOT_DIR, "data", "static_data")
        img = PIL.Image.open(
            Path(static_data_path, f"{extra_data['Moon']['Type'].replace('Satellite (Phase: ', '').replace(')', '').lower().replace(' ', '_')}.jpg")
        )
        Logger.log("Generating image text.")
        overlay_txt = [
            f"Name: Moon",
            f"Type: {extra_data['Moon']['Type']}",
            f"Constellation: {extra_data['Moon']['Constellation']}",
            f"Brightness: {extra_data['Moon']['Brightness']}",
            f"Distance: {extra_data['Moon']['Distance']} Pm",
            conv_str,
        ]
        img = add_text(img, overlay_txt)
        Logger.log(f"Adding edited image of {celestial_obj} to cache file...")
        img.save(
            fp=Path(
                Const.SLIDESHOW_DIR,
                "PySkySlideshow",
                "garbage",
                f"{celestial_obj}.temp.jpg",
            )
        )

        
        img.save(
            fp=Path(
                Const.SLIDESHOW_DIR,
                "PySkySlideshow",
                f"{celestial_obj.title().replace(' ', '_')}_{extra_data['Moon']['Type'].replace('Satellite (Phase: ', '').replace(')', '').lower().replace(' ', '_')}_{Const.START_YEAR}-{Const.START_MONTH}-{Const.START_DAY}.pdf",
            ),
            format="pdf",
        )

    elif celestial_obj.lower() in cache_file:
        Logger.log(f"Overlaying text for {celestial_obj}")
        if not os.path.isdir(Path(Const.SLIDESHOW_DIR, "PySkySlideshow", "garbage")):
            Logger.log("Garbage directory not found! Creating it.", 30)
            os.makedirs(Path(Const.SLIDESHOW_DIR, "PySkySlideshow", "garbage"))
        Logger.log("Loading image data.")
        img = PIL.Image.open(
            Path(
                Const.SLIDESHOW_DIR,
                "PySkySlideshow",
                "garbage",
                f"{celestial_obj}.temp.jpg",
            )
        )
        Logger.log("Generating image text.")
        overlay_txt = [
            f"Name: {celestial_obj.capitalize()}",
            f"Type: {cache_file[celestial_obj]['Type']}",
            f"Constellation: {cache_file[celestial_obj]['Constellation']}",
            f"Brightness: {cache_file[celestial_obj]['Brightness']}",
            f"Distance: {cache_file[celestial_obj]['Distance']} Pm",
            conv_str,
        ]
        img = add_text(img, overlay_txt)
        Logger.log(f"Adding edited image of {celestial_obj} to cache file...")
        img.save(
            fp=Path(
                Const.SLIDESHOW_DIR,
                "PySkySlideshow",
                "garbage",
                f"{celestial_obj}.temp.jpg",
            )
        )

        with open(Path(Const.ROOT_DIR, "data", "cache"), "w") as json_out:
            Logger.log("Saving edited cache file...")
            json.dump(cache_file, json_out)
            Logger.log("Edited cache file saved!")
            img.save(
                fp=Path(
                    Const.SLIDESHOW_DIR,
                    "PySkySlideshow",
                    f"{celestial_obj.title().replace(' ', '_')}.pdf",
                ),
                format="pdf",
            )


def add_text(img: object, overlay_txt: list) -> object:
    """
    Add the text on the image.
    :param img: PIL.Image object to overlay text on.
    :param overlay_txt: List of string to overlay on the image.
    :return: PIL.Image object with the overlaid text.
    """
    # only save the height of the image
    try:
        _, img_h = img.size
    except AttributeError:
        Logger.log(f"Error opening {img}", 50)

    Logger.log("Overlaying text to image...")
    fonts = [
        Path(Const.ROOT_DIR, "data", "res") / f
        for f in os.listdir(Path(Const.ROOT_DIR, "data", "res"))
        if ".ttf" in f
    ]
    overlaid = PIL.ImageDraw.Draw(img, mode="RGBA")
    if len(fonts) >= 1:
        fnt_path = Path(Const.ROOT_DIR, "data", "res") / fonts[0]
        fnt = PIL.ImageFont.truetype(str(fnt_path), int(img_h / 33))
        overlaid.multiline_text(
            xy=(20, int(img_h * 0.75)),  # xy for the text to be overlaid
            text="\n".join(overlay_txt),  # concats all strings in the list
            fill=(255, 255, 255, 100),  # white text with alpha=100
            font=fnt,
            stroke_width=1,  # thickness of the stroke
            stroke_fill=(0, 0, 0, 100),  # black stroke with alpha=100
            spacing=2.0,  # in between each new line
            align="left",
        )
    else:
        overlaid.multiline_text(
            xy=(10, int(img_h * 0.75)),  # xy for the text to be overlaid
            text="\n".join(overlay_txt),  # concats all strings in the list
            fill=(255, 255, 255, 100),  # white text with alpha=100
            spacing=2.0,  # in between each new line
            align="left",
        )

    return img


def img_garbage_collection():
    for img in [
        Path(Const.SLIDESHOW_DIR, "PySkySlideshow", "garbage") / f
        for f in os.listdir(Path(Const.ROOT_DIR, "data"))
        if ".temp.jpg" in f
    ]:
        os.remove(img)
