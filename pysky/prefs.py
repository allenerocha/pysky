"""This module is called at application launch and checks for user
preferences and applies the cache rules to the cache file and saves it"""
import json
import logging
import os.path
from logging import critical, error, info, warning
from pathlib import Path

from tqdm import tqdm


def check_integrity(root_dir: str):
    """
    This module checks if there is a preference file
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    info("Checking project integrity...")
    info("Checking for data directory...")
    if not os.path.isdir(f"{root_dir}/data"):
        warning("Data directory not found.\nCreating data directory and cache file...")
        os.makedirs(f"{root_dir}/data")
        with open(f"{root_dir}/data/cache", "w") as cache_file:
            cache_file.write("{}")
        info("Data directory and cache file created!")

    else:
        info("Data directory found!")
        info("Checking for chache file...")
        if os.path.isfile(f"{root_dir}/data/cache"):
            info("Cache file found!")
            clean_cache(root_dir)
        else:
            warning("Cache file not found.")
            info("Creating cache file...")
            with open(f"{root_dir}/data/cache", "w") as cache_file:
                cache_file.write("{}")
            info("Created cache file!")

    info(f"Searching in `{root_dir}/data/` for `VisibleCadwellCatalog.json`...")
    if not os.path.isfile(f"{root_dir}/data/VisibleCadwellCatalog.json"):
        error(
            f"VisibleCadwellCatalog.json not found in the directory `{root_dir}/data/`!\nThe Application will not automatically search for these objects unless they are redownloaded.\n"
        )
    else:
        info(f"VisibleCadwellCatalog.json was found!\n")

    info(f"Searching in `{root_dir}/data/` `VisibleMessierCatalog.json`...")
    if not os.path.isfile(f"{root_dir}/data/VisibleMessierCatalog.json"):
        error(
            f"VisibleMessierCatalog.json not found in the directory `{root_dir}/data/`!\nThe Application will not automatically search for these objects unless they are redownloaded.\n"
        )
    else:
        info(f"VisibleMessierCatalog.json was found!\n")

    info("Checking for slideshow directory...")
    if not os.path.isdir(f"{Path.home()}/PySkySlideshow"):
        warning("Slideshow directory not found.")

        info("Creating slideshow directory...")
        os.makedirs(f"{Path.home()}/PySkySlideshow")
        info("Created slideshow directory!")

    else:
        info("Slideshow directory found!")
    info("Project integrity verified.\n")


def clean_cache(root_dir: str):
    """
    Reads prefs files and calls the prune function to remove planets
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )

    info("Cleaning cache...")
    try:
        cache_file = json.loads(open(f"{root_dir}/data/cache", "r").read())
    except json.decoder.JSONDecodeError as e:
        error(f"\nError reading cache file. Generating emptying cache...\n{str(e)}\n")
        with open(f"{root_dir}/data/cache", "w") as cache_file:
            cache_file.write("{}")
            info("Created cache file!")
        return

    cache_file_aux = dict()

    # Iterate over the cache file looking for non-planets
    for celestial_object, attributes in tqdm(cache_file.items()):
        for key, value in tqdm(attributes.items()):
            # Non-planet found adding to auxilary dictionary
            if key == "type" and value != "planet":
                cache_file_aux[celestial_object] = attributes
                continue
    info("Cache cleaned!\n")

    info("Saving changes to cache file...")
    with open(f"{root_dir}/data/cache", "w") as json_out:
        json.dump(cache_file_aux, json_out, indent=4, sort_keys=True)
        info("Changes saved to cache file!\n")


def read_user_prefs(root_dir: str) -> list:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )
    info(f"Searching `{root_dir}/data/` for `user_prefs.cfg`...")
    if not os.path.isfile(f"{root_dir}/data/user_prefs.cfg"):
        critical(
            f"User preferences file `user_prefs.cfg` not found in the directory `{root_dir}/data/`!\nApplication will continue, only looking for planets, Messier catalog, and Cadwell catalog objects.\n"
        )
        return None
    else:
        info("User preferences file `user_prefs.cfg` found!")
        info("Parsing `user_prefs.cfg`...")
        with open(f"{root_dir}/data/user_prefs.cfg", "r") as u_prefs_file:
            u_prefs_lines = [
                line.strip()
                for line in u_prefs_file.readlines()
                if len(line.strip()) > 0 and line.strip()[0] != "#"
            ]
            info("Finished parsing user preferences!\n")
        return u_prefs_lines
