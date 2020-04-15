"""This module is called at application launch and checks for user
preferences and applies the cache rules to the cache file and saves it"""
import json
import logging
import os.path
import sys
from logging import warning, error, info


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
        os.mkdir(f"{root_dir}/data")
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

    info("Checking for slideshow directory...")
    if not os.path.isdir(f"{root_dir}/slideshow"):
        warning("Slideshow directory not found.")

        info("Creating slideshow directory...")
        os.path.mkdir(f"{root_dir}/slideshow")
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
    for celestial_object, attributes in cache_file.items():
        for key, value in attributes.items():
            # Non-planet found adding to auxilary dictionary
            if key == "type" and value != "planet":
                cache_file_aux[celestial_object] = attributes
                continue
    info("Cache cleaned!\n")

    info("Saving changes to cache file...")
    with open(f"{root_dir}/data/cache", "w") as json_out:
        json.dump(cache_file_aux, json_out, indent=4, sort_keys=True)
        info("Changes saved to cache file!\n")


def print_cache(root_dir):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{root_dir}/data/log"), logging.StreamHandler()],
    )
    # Iterate keys
    for key, value in cache_file.items():
        info(f"{key} =>")
        try:
            for subkey, subvalue in value.items():
                try:
                    for subsubkey, subsubvalue in subvalue.items():
                        if subsubkey != "base64":
                            info(f"\t\t{subsubkey} => {subsubvalue}")
                except:
                    info(f"\t{subkey} => {subvalue}")
        except:
            info(f"k:{key} => v:{value}")
