"""This module will be used to overlay information of the
celestial body over image of the celestial body using PIL"""
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import slideshow.slideshow

def add_text(img: object, overlay_text: list, slide_show: object) -> object:
    """
    This adds text to the image
    :img: Image file to overlay the text
    :overlay_text: List of text to overlay on the image
    :return: None
    """

    """
    overlay_test -> [name, brightess]
    """


    _, img_h = img.size

    overlayed = PIL.ImageDraw.Draw(img, mode='RGBA')
    overlayed.multiline_text(
                            xy=(10,int(img_h*0.8)),
                            text="\n".join(overlay_text),#concats all passed strings in the list
                            fill=(255, 255, 255, 100),#white text with alpha=100
                            font=PIL.ImageFont.truetype("aakar-medium.ttf", 16),
                            stroke_width=1,
                            stroke_fill=(0, 0, 0, 100),#black stroke with alpha=100
                            spacing=1,#in between each new line
                            align="left"
                            )
    return(img)
