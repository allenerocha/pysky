"""This module will be used to overlay information of the
celestial body over image of the celestial body using PIL"""
import json
import base64
import os
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


def add_text(img: object, overlay_text: list) -> object:
    """
    This adds text to the image
    :img: Image file to overlay the text
    :overlay_text: List of text to overlay on the image
    :return: None
    """

    """
    overlay_text -> [name, brightess]
    """

    #only save the height of the image
    _, img_h = img.size

    cache_file = json.loads(open("data/cache", "r").read())
    print(f"Overlaying text to image...")
    overlayed = PIL.ImageDraw.Draw(img, mode='RGBA')
    overlayed.multiline_text(
                            xy=(10,int(img_h*0.8)),#xy of the location for the text to  be overlayed
                            text="\n".join(overlay_text),#concats all passed strings in the list
                            fill=(255, 255, 255, 100),#white text with alpha=100
                            stroke_width=1,#thickness of the stoke
                            stroke_fill=(0, 0, 0, 100),#black stroke with alpha=100
                            spacing=1,#in between each new line
                            align="left"
                            )

    print("Adding edited image to cache file...")
    img.save(fp='data/temp', format="PNG")
    img_bytes = base64.b64encode(open("data/temp", "rb").read())
    celestial_obj = overlay_text[0][6:]
    # write the edited image to the cache file
    cache_file[celestial_obj]["image"]["base64"] = str(img_bytes)[1:]
    print("Edited image added to cache file!")

    with open("data/cache", "w") as json_out:
        print("Saving edited cache file...")
        json.dump(cache_file, json_out)
        os.remove("data/temp")
        print("Edited cache file saved!")

