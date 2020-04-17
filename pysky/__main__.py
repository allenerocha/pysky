#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The main entry point. Invoke as `pysky' or python -m pysky.
"""
import sys


def main():
    from .core import invoke

    invoke(sys.argv[1:])


if __name__ == "__main__":
    main()
