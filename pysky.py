#!/usr/bin/env python3
import sys
import json
import io
import base64
import PIL.Image
import utils.skyview
import utils.astro_info
import slideshow.image_manipulation
import slideshow.slideshow


def main():
    """
    """

    #db_calls('neptune', 'venus', 'saturn')

    # todo pass a window of time {start: YEAR-DAY-MON H:M, end: YEAR-DAY-MON H:M}:
    # todo check endpoints <==== DONE
    # todo try-catch for successful server connection <==== DONE
    # todo download brightness from simbad if successfully connected <==== DONE
    # todo download image from skyview/nasa site if successfully connected <==== DONE
    # todo overlay celesital statistics on the image <==== WIP
    # todo add overlayed image to slideshow queue
    # todo play slideshow

    # todo make sure not to repeatedly add object information if it is already stored in the cache

    # Checks in the passed body or list of bodies are in the emphemeries Quantity
    EPHEMERIES_BODIES = utils.astro_info.get_bodies('neptune', 'venus', 'polaris', 'saturn')

    cache_file = json.loads(open("cache/data", "r").read())

    for body in EPHEMERIES_BODIES:
        print(body)
        COORDS = utils.astro_info.get_info(body)
        cache_file[f"{body}"] = {}
        cache_file[f"{body}"]["coordinates"] = {"ra": [COORDS[0], COORDS[1], COORDS[2]], "dec": { "degree": COORDS[3], "radian": COORDS[4]}, "cartesian": [str(COORDS[5]), str(COORDS[6]), str(COORDS[7])]}
    with open("cache/data", "w") as json_out:
        json.dump(cache_file, json_out)
    sys.exit()


def db_calls(*args):
    # creates an empty slide show queue
    slide_show = slideshow.slideshow.SlideShow(None)

    celestial_objs = list(args)

    print(celestial_objs)
    sys.exit()
    for celestial_obj in celestial_objs:
        # try to get image and data of the object
        utils.skyview.get_img(celestial_obj, 480, 480, 3.5, "Linear")
        cache_file = json.loads(open("cache/data", "r").read())

        # decode the image from the cache file from b64 to bytes
        decoded_img = base64.b64decode(cache_file[celestial_obj]['image']['base64'][1:-1])

        # save the returned image containing the overlayed information
        overlayed_img = slideshow.image_manipulation.add_text(
                                                                PIL.Image.open(io.BytesIO(decoded_img)),
                                                                [
                                                                    f"Name: {celestial_obj}",
                                                                    f"Brightness: {cache_file[celestial_obj]['brightness']}"
                                                                ],
                                                                slide_show
                                                            )

        # add the returned image to the slide show queue
        slide_show.add_image(overlayed_img)


if __name__ == '__main__':
    main()

