"""This module is called at application launch and checks for user
preferences and applies the cache rules to the cache file and saves it"""
import os.path
import sys
import json


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
            pass
            #clean_cache()
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
    # todo load data/prefs
    # todo check cache rules
    # todo iterate through the cache and apply rules
    # todo call prune
    # todo dump cache json to data/cache
    print("Cleaning cache...")
    cache_file = json.loads(open("data/cache", "r").read())

    print("Cache cleaned!\n")

def prune(key: str) -> dict:
    """
    Removes a given key from the cache
    """
    # todo pop/delete the key in the passed dictoionary
    pass


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

