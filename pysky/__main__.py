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
    from . import __title__
    from . import __description__
    from . import __author__
    from . import __email__
    from . import __version__
    from . import __licence__
    from . import __url__

    print(
        f"{__title__}\t{__licence__}\t{__version__}\n"
        + f"{__description__}\n"
        + f"{__author__}\t{__email__}\n"
        + f"Source code at: {__url__}\n"
    )
    main()
