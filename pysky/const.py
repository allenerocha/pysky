# -*- encoding: utf-8 -*-
"""Constant variables to be accessed across the application."""
import os.path


class Const(object):
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    SLIDESHOW_DIR = ""
    THREADS = 1
    VERBOSITY = 20
    START_YEAR = ""
    START_DAY = ""
    START_MONTH = ""
    START_TIME = ""
    END_YEAR = ""
    END_DAY = ""
    END_MONTH = ""
    END_TIME = ""
    LATITUDE = 0.0
    LONGITUDE = 0.0
    ELEVATION = 0.0
    MIN_V = 4.5
