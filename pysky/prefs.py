"""This module is called at application launch and checks for user
preferences and applies the cache rules to the cache file and saves it"""
import json
import os.path
from pathlib import Path

from tqdm import tqdm

from .const import Const
from .logger import Logger


def check_integrity():
    """
    This module checks if there is a preference file
    """

    Logger.log("Checking project integrity...")
    Logger.log("Checking for data directory...")
    if not os.path.isdir(Path(Const.ROOT_DIR, "data")):
        Logger.log("Data directory not found.", 30)
        Logger.log("Creating data directory and cache file...", 30)
        os.makedirs(Path(Const.ROOT_DIR, "data"))
        with open(Path(Const.ROOT_DIR, "data", "cache"), "w") as cache_file:
            cache_file.write("{}")
        Logger.log("Data directory and cache file created!")

    else:
        Logger.log("Data directory found!")
        Logger.log("Checking for cache file...")
        if os.path.isfile(Path(Const.ROOT_DIR, "data", "cache")):
            Logger.log("Cache file found!")
            clean_cache()
        else:
            Logger.log("Cache file not found.", 30)
            Logger.log("Creating cache file...")
            with open(Path(Const.ROOT_DIR, "data", "cache"), "w") as cache_file:
                cache_file.write("{}")
            Logger.log("Created cache file!")

    Logger.log(
        f"Searching in `{Const.ROOT_DIR}/data/` " + "for `CaldwellCatalogue.json`..."
    )
    if not os.path.isfile(Path(Const.ROOT_DIR, "data", "CaldwellCatalogue.json")):
        Logger.log(
            "CaldwellCatalogue.json not found in the directory "
            + f"`{Const.ROOT_DIR}/data/`!",
            40,
        )
        Logger.log(
            "The Application will not automatically search "
            + "for these objects unless they are redownloaded.\n",
            40,
        )
    else:
        Logger.log("CaldwellCatalogue.json was found!\n")

    Logger.log(
        f"Searching in `{Const.ROOT_DIR}/data/` " + "for `MessierCatalogue.json`..."
    )
    if not os.path.isfile(Path(Const.ROOT_DIR, "data", "MessierCatalogue.json")):
        Logger.log(
            "MessierCatalogue.json not found in the directory "
            + f"`{Const.ROOT_DIR}/data/`!",
            40,
        )
        Logger.log(
            "The Application will not automatically search "
            + "for these objects unless they are redownloaded.\n",
            40,
        )
    else:
        Logger.log("MessierCatalogue.json was found!\n")


def clean_cache():
    """
    Reads prefs files and calls the prune function to remove planets
    """

    Logger.log("Cleaning cache...")
    try:
        cache_file = json.loads(open(Path(Const.ROOT_DIR, "data", "cache"), "r").read())
    except json.decoder.JSONDecodeError as json_dec_err:
        Logger.log("\nError reading cache file.", 40)
        Logger.log(f"Generating emptying cache...\n{str(json_dec_err)}\n", 40)
        with open(Path(Const.ROOT_DIR, "data", "cache"), "w") as cache_file:
            cache_file.write("{}")
            Logger.log("Created cache file!")
        return

    cache_file_aux = dict()

    # Iterate over the cache file looking for non-planets
    for celestial_object, attributes in tqdm(cache_file.items()):
        for key, value in tqdm(attributes.items()):
            # Non-planet found adding to auxiliary dictionary
            if key == "type" and value != "planet":
                cache_file_aux[celestial_object] = attributes
    Logger.log("Cache cleaned!\n")

    Logger.log("Saving changes to cache file...")
    with open(Path(Const.ROOT_DIR, "data", "cache"), "w") as json_out:
        json.dump(cache_file_aux, json_out, indent=4, sort_keys=True)
        Logger.log("Changes saved to cache file!\n")


def read_user_prefs():
    """
    Parse the user preferences, if they exist.
    """
    Logger.log(f"Searching `{Const.ROOT_DIR}/data/` for `user_prefs.cfg`...")
    if not os.path.isfile(Path(Const.ROOT_DIR, "data", "user_prefs.cfg")):
        Logger.log(
            "User preferences file `user_prefs.cfg` not found "
            + f"in the directory `{Const.ROOT_DIR}/data/`!",
            50,
        )
        Logger.log(
            "Application will continue, only looking for planets, "
            + "Messier catalog, and Caldwell catalog objects.\n",
            50,
        )
        return None
    Logger.log("User preferences file `user_prefs.cfg` found!")
    Logger.log("Parsing `user_prefs.cfg`...")
    with open(Path(Const.ROOT_DIR, "data", "user_prefs.cfg"), "r") as u_prefs_file:
        user_objs = list()
        user_save_loc = str()
        for line in u_prefs_file.readlines():
            if len(line.strip()) > 0 and line.strip()[0] != "#":
                if "slideshow_dir" in line.strip().lower():
                    user_save_loc = line.strip().split("=")[1].strip()
                elif "latitude" in line.strip().lower():
                    Const.LATITUDE = float(line.strip().split("=")[1].strip())
                elif "longitude" in line.strip().lower():
                    Const.LONGITUDE = float(line.strip().split("=")[1].strip())
                elif "elevation" in line.strip().lower():
                    Const.ELEVATION = float(line.strip().split("=")[1].strip())
                elif "v=" in line.strip().replace(" ", "").lower():
                    Const.MIN_V = float(line.strip().split("=")[1].strip())
                elif "secz_max=" in line.strip().replace(" ", "").lower():
                    Const.SECZ_MAX = float(line.strip().split("=")[1].strip())
                else:
                    if "," not in line.strip():
                        user_objs.append(line.strip())
                    else:
                        user_objs.extend(line.strip().split(","))

        user_objs = list(map(str.strip, user_objs))

        Logger.log("Finished parsing user preferences!\n")

    if user_save_loc == "":
        user_save_loc = str(Path.home())

    Const.SLIDESHOW_DIR = user_save_loc
    Logger.log("Checking for slideshow directory...")
    if not os.path.isdir(Path(Const.SLIDESHOW_DIR, "PySkySlideshow")):
        Logger.log("Slideshow directory not found.", 30)

        Logger.log("Creating slideshow directory...")
        os.makedirs(Path(Const.SLIDESHOW_DIR, "PySkySlideshow"))
        Logger.log(f"Created slideshow directory in {Const.SLIDESHOW_DIR}!")

    else:
        Logger.log("Slideshow directory found!")

    return user_objs
