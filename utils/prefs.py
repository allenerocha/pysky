"""This module is called at application launch and checks for user
preferences and applies the cache rules to the cache file and saves it"""
import json
import os.path
import sys


def check_integrity():
    """
    This module checks if there is a preference file
    """
    print("Checking project integrity...")
    print("Checking for data directory...")
    if not os.path.isdir("data"):
        print("Data directory not found.\nCreating data directory and cache file...")
        os.mkdir("data")
        with open("data/cache", "w") as cache_file:
            cache_file.write("{}")
        print("Data directory and cache file created!")

    else:
        print("Data directory found!")
        print("Checking for chache file...")
        if os.path.isfile("data/cache"):
            print("Cache file found!")
            clean_cache()
        else:
            print("Cache file not found.")
            print("Creating cache file...")
            with open("data/cache", "w") as cache_file:
                cache_file.write("{}")
            print("Created cache file!")

    print("Checking for slideshow directory...")
    if not os.path.isdir("slideshow"):
        print("Slideshow directory not found.")

        print("Creating slideshow directory...")
        os.path.mkdir("slideshow")
        print("Created slideshow directory!")

    else:
        print("Slideshow directory found!")
    print("Project integrity verified.\n")


def clean_cache():
    """
    Reads prefs files and calls the prune function to remove planets
    """
    print("Cleaning cache...")
    try:
        cache_file = json.loads(open("data/cache", "r").read())
    except json.decoder.JSONDecodeError as e:
        print(f"\nError reading cache file. Generating emptying cache...\n{str(e)}\n")
        with open("data/cache", "w") as cache_file:
            cache_file.write("{}")
            print("Created cache file!")
        return

    cache_file_aux = dict()

    # Iterate over the cache file looking for non-planets
    for celestial_object, attributes in cache_file.items():
        for key, value in attributes.items():
            # Non-planet found adding to auxilary dictionary
            if key == "type" and value != "planet":
                cache_file_aux[celestial_object] = attributes
                continue
    print("Cache cleaned!\n")

    print("Saving changes to cache file...")
    with open("data/cache", "w") as json_out:
        json.dump(cache_file_aux, json_out, indent=4, sort_keys=True)
        print("Changes saved to cache file!\n")


def print_cache():
    # Iterate keys
    for key, value in cache_file.items():
        print(f"{key} =>")
        try:
            for subkey, subvalue in value.items():
                try:
                    for subsubkey, subsubvalue in subvalue.items():
                        if subsubkey != "base64":
                            print(f"\t\t{subsubkey} => {subsubvalue}")
                except:
                    print(f"\t{subkey} => {subvalue}")
        except:
            print(f"k:{key} => v:{value}")
