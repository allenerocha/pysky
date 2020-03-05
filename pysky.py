#!/usr/bin/env python3
import sys
import json
import io
import base64
import PIL.Image
import utils.skyview
import slideshow.image_manipulation


def main():
    """
    arg[1] celestial_obj
    arg[2] width
    arg[3] height
    arg[4] image_size
    arg[5] b_scale
    :return:
    """

    # todo compare date with previous run date
    # todo check endpoints
    # todo try-catch for successful server connection
    # todo download brightness from simbad if successfully connected
    # todo download image from skyview/nasa site if successfully connected
    # todo overlay celesital statistics on the image
    # todo add overlayed image to slideshow queue
    # todo play slideshow

    utils.skyview.get_img(sys.argv[1], int(sys.argv[2]),
                          int(sys.argv[3]), float(sys.argv[4]), sys.argv[5])
    cache_file = json.loads(open("cache/data", "r").read())
    decoded_img = base64.b64decode(cache_file[sys.argv[1]]['image']['base64'][1:-1])
    slideshow.image_manipulation.add_text(PIL.Image.open(io.BytesIO(decoded_img)), [f"Name: {sys.argv[1]}", f"Brightness: {cache_file[sys.argv[1]]['brightness']}"])



if __name__ == '__main__':
    main()
