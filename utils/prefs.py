"""This module is called at application launch and checks for user
preferences and applies the cache rules to the cache file and saves it"""
import os.path
import sys
import json


def check_prefs():
    """
    This module checks if there is a preference file
    """
    if os.path.isfile('data/prefs'):
        clean_cache()
    else:
        create_prefs()


def create_prefs():
    """
    This module is used to create prefs file
    """
    # todo open dictionary of possible options
    # todo display options
    # todo user selects options
    # todo dump json file to data/prefs
    os.makedir("data")
    with open("data/prefs", "w") as cache_file:
        cache_file.write("{}")


def clean_cache():
    """
    Reads prefs files and calls the prune function to remove certain keys
    """
    # todo load data/prefs
    # todo check cache rules
    # todo iterate through the cache and apply rules
    # todo call prune
    # todo dump cache json to data/cache
    pass


def prune():
    """
    Removes a given key from the cache
    """
    # todo pop/delete the key in the passed dictoionary
    pass


