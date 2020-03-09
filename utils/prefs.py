import os.path
import sys

# todo check for prefs file
# todo if doesn't exist, make one
# todo prefs_check() -> read_prefs() -> cache_rules() -> cache_clean()
#                    -> guided_prefs_creation()

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
    print('true')
    sys.exit()
    pass


def clean_cache():
    """
    Reads prefs files and calls the prune function to remove certain keys
    """
    pass


def prune():
    """
    Removes a given key from the cache
    """
    pass


