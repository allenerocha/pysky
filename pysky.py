#!/usr/bin/env python3
import sys
import json
import io
import base64
import PIL.Image
import utils.skyview
import slideshow.image_manipulation
import slideshow.slideshow

def main():
    """
    arg[1] celestial_obj
    arg[2] width
    arg[3] height
    arg[4] image_size
    arg[5] b_scale
    :return:
    """

    # todo check endpoints <==== DONE
    # todo try-catch for successful server connection <==== DONE
    # todo download brightness from simbad if successfully connected <==== DONE
    # todo download image from skyview/nasa site if successfully connected <==== DONE
    # todo overlay celesital statistics on the image <==== WIP
    # todo add overlayed image to slideshow queue
    # todo play slideshow

    # todo make sure not to repeatedly add object information if it is already stored in the cache

    # creates an empty slide show queue
    slide_show = slideshow.slideshow.SlideShow(None)

    # try to get image and data of the object
    utils.skyview.get_img(
                            sys.argv[1],
                            int(sys.argv[2]),
                            int(sys.argv[3]),
                            float(sys.argv[4]),
                            sys.argv[5]
                        )
    cache_file = json.loads(open("cache/data", "r").read())

    # decode the image from the cache file from b64 to bytes
    decoded_img = base64.b64decode(cache_file[sys.argv[1]]['image']['base64'][1:-1])

    # save the returned image containing the overlayed information
    overlayed_img = slideshow.image_manipulation.add_text(
                                                            PIL.Image.open(io.BytesIO(decoded_img)),
                                                            [
                                                                f"Name: {sys.argv[1]}",
                                                                f"Brightness: {cache_file[sys.argv[1]]['brightness']}"
                                                            ],
                                                            slide_show
                                                        )

    # add the returned image to the slide show queue
    slide_show.add_image(overlayed_img)


if __name__ == '__main__':
    main()

