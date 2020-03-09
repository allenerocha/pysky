#!/usr/bin/env python3
import sys
import json
import time
import io
import os.path
import base64
import PIL.Image
import utils.skyview
import utils.astro_info
import utils.objectfilter
import slideshow.image_manipulation
import slideshow.slideshow
import utils.prefs


def main():
    """
    """
    #utils.prefs.check_prefs()

    celestial_objs = utils.objectfilter.emphemeries_filter('venus', 'polaris', 'neptune', 'vega', 'saturn', 'mars')
    STARS = celestial_objs[0]
    EPHEMERIES_BODIES = celestial_objs[1]
    db_calls(STARS)

    # todo pass a window of time {start: YEAR-DAY-MON H:M, end: YEAR-DAY-MON H:M}:
    # todo check endpoints <==== DONE
    # todo try-catch for successful server connection <==== DONE
    # todo download brightness from simbad if successfully connected <==== DONE
    # todo download image from skyview/nasa site if successfully connected <==== DONE
    # todo overlay celesital statistics on the image <==== WIP
    # todo add overlayed image to slideshow queue
    # todo play slideshow *****
    # todo make sure not to repeatedly add object information if it is already stored in the cache ******

    # Checks in the passed body or list of bodies are in the emphemeries Quantity

    cache_file = json.loads(open("data/cache", "r").read())

    for body in EPHEMERIES_BODIES:
        COORDS = utils.astro_info.get_info(body)
        cache_file[f"{body}"] = {}
        cache_file[f"{body}"]["type"] = "planet"
        cache_file[f"{body}"]["created"] = time.strftime("%Y-%d-%m %H:%M", time.gmtime())
        cache_file[f"{body}"]["coordinates"] = {
                                                    "ra": [
                                                            COORDS[0],
                                                            COORDS[1],
                                                            COORDS[2]
                                                        ],
                                                    "dec": {
                                                            "degree": COORDS[3],
                                                            "radian": COORDS[4]
                                                            },
                                                    "cartesian": [
                                                            str(COORDS[5]),
                                                            str(COORDS[6]),
                                                            str(COORDS[7])
                                                                ]
                                                }
    with open("data/cache", "w") as json_out:
        json.dump(cache_file, json_out, indent=4, sort_keys=True)


def db_calls(celestial_objs):
    # creates an empty slide show queue
    slide_show = slideshow.slideshow.SlideShow(None)

    for celestial_obj in celestial_objs:
        # try to get image and data of the object
        utils.skyview.get_img(celestial_obj, 480, 480, 3.5, "Linear")
        cache_file = json.loads(open("data/cache", "r").read())

        # decode the image from the cache file from b64 to bytes
        decoded_img = base64.b64decode(cache_file[celestial_obj]['image']['base64'][1:-1])

        # save the returned image containing the overlayed information
        slideshow.image_manipulation.add_text(PIL.Image.open(io.BytesIO(decoded_img)), [
                                                                                            f"Name: {celestial_obj}",
                                                                                            f"Constellation: {cache_file[celestial_obj]['constellation']}",
                                                                                            f"Brightness: {cache_file[celestial_obj]['brightness']}"
                                                                                        ]
                                                                                    )

        # add the returned image to the slide show queue
        # slide_show.add_image(overlayed_img)
        # slide_show.play()


if __name__ == '__main__':
    if not os.path.isfile('data/cache'):
        with open('data/cache', 'w') as cache:
            cache.write("{}")
    main()

