# -*- encoding: utf-8 -*-
"""Constant variables to be accessed across the application."""
import os.path


class Const(object):
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    SLIDESHOW_DIR = ""
    THREADS = 1
    VERBOSITY = 20

