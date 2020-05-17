"""This module is called at application launch and checks for user
preferences and applies the cache rules to the cache file and saves it"""
import json
from .logger import Logger
import os.path
from pathlib import Path

from tqdm import tqdm


def check_integrity(root_dir: str):
    """
    This module checks if there is a preference file
    """

    Logger.log("Checking project integrity...")
    Logger.log("Checking for data directory...")
    if not os.path.isdir(f"{root_dir}/data"):
        Logger.log("Data directory not found.", 30)
        Logger.log("Creating data directory and cache file...", 30)
        os.makedirs(f"{root_dir}/data")
        with open(f"{root_dir}/data/cache", "w") as cache_file:
            cache_file.write("{}")
        Logger.log("Data directory and cache file created!")

    else:
        Logger.log("Data directory found!")
        Logger.log("Checking for chache file...")
        if os.path.isfile(f"{root_dir}/data/cache"):
            Logger.log("Cache file found!")
            clean_cache(root_dir)
        else:
            Logger.log("Cache file not found.", 30)
            Logger.log("Creating cache file...")
            with open(f"{root_dir}/data/cache", "w") as cache_file:
                cache_file.write("{}")
            Logger.log("Created cache file!")

    Logger.log(
        f"Searching in `{root_dir}/data/` for `VisibleCaldwellCatalogue.json`..."
    )
    if not os.path.isfile(f"{root_dir}/data/VisibleCaldwellCatalogue.json"):
        Logger.log(
            "VisibleCaldwellCatalogue.json not found in the directory " +
            f"`{root_dir}/data/`!",
            40
        )
        Logger.log(
            "The Application will not automatically search " +
            "for these objects unless they are redownloaded.\n",
            40
        )
    else:
        Logger.log("VisibleCaldwellCatalogue.json was found!\n")

    Logger.log(
        f"Searching in `{root_dir}/data/` for `VisibleMessierCatalog.json`..."
    )
    if not os.path.isfile(f"{root_dir}/data/VisibleMessierCatalog.json"):
        Logger.log(
            "VisibleMessierCatalog.json not found in the directory " +
            f"`{root_dir}/data/`!",
            40
        )
        Logger.log(
            "The Application will not automatically search " +
            "for these objects unless they are redownloaded.\n",
            40
        )
    else:
        Logger.log(f"VisibleMessierCatalog.json was found!\n")

    Logger.log("Checking for slideshow directory...")
    if not os.path.isdir(f"{Path.home()}/PySkySlideshow"):
        Logger.log("Slideshow directory not found.", 30)

        Logger.log("Creating slideshow directory...")
        os.makedirs(f"{Path.home()}/PySkySlideshow")
        Logger.log("Created slideshow directory!")

    else:
        Logger.log("Slideshow directory found!")
    Logger.log("Project integrity verified.\n")


def clean_cache(root_dir: str):
    """
    Reads prefs files and calls the prune function to remove planets
    """

    Logger.log("Cleaning cache...")
    try:
        cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())
    except json.decoder.JSONDecodeError as e:
        Logger.log(
            "\nError reading cache file.",
            40
            )
        Logger.log(
            f"Generating emptying cache...\n{str(e)}\n",
            40
        )
        with open(f"{root_dir}/data/cache", "w") as cache_file:
            cache_file.write("{}")
            Logger.log("Created cache file!")
        return

    cache_file_aux = dict()

    # Iterate over the cache file looking for non-planets
    for celestial_object, attributes in tqdm(cache_file.items()):
        for key, value in tqdm(attributes.items()):
            # Non-planet found adding to auxilary dictionary
            if key == "type" and value != "planet":
                cache_file_aux[celestial_object] = attributes
                continue
    Logger.log("Cache cleaned!\n")

    Logger.log("Saving changes to cache file...")
    with open(f"{root_dir}/data/cache", "w") as json_out:
        json.dump(cache_file_aux, json_out, indent=4, sort_keys=True)
        Logger.log("Changes saved to cache file!\n")


def read_user_prefs(root_dir: str):
    Logger.log(f"Searching `{root_dir}/data/` for `user_prefs.cfg`...")
    if not os.path.isfile(f"{root_dir}/data/user_prefs.cfg"):
        Logger.log(
            "User preferences file `user_prefs.cfg` not found " +
            f"in the directory `{root_dir}/data/`!",
            50
        )
        Logger.log(
            "Application will continue, only looking for planets, " +
            "Messier catalog, and Caldwell catalog objects.\n",
            50
        )
        return None
    else:
        Logger.log("User preferences file `user_prefs.cfg` found!")
        Logger.log("Parsing `user_prefs.cfg`...")
        with open(f"{root_dir}/data/user_prefs.cfg", "r") as u_prefs_file:
            u_prefs_lines = [
                line.strip()
                for line in u_prefs_file.readlines()
                if len(line.strip()) > 0 and line.strip()[0] != "#"
            ]
            Logger.log("Finished parsing user preferences!\n")
        return u_prefs_lines
