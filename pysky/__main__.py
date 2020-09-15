#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main entry point.
Invoke as `pysky' or python -m pysky.
"""


def main():
    """Invokes the main function."""
    from .core import invoke

    invoke()


if __name__ == "__main__":
    main()
