# -*- encoding: utf-8 -*-
"""This module is able contains the method to log all output to a log file."""
import logging
from logging import critical, error, info, warning, debug
from .const import Const


class Logger:
    def log(msg: str, lvl=20):
        """Initialize the logger using the constants defined in the const."""
        logging.basicConfig(
            level=Const.VERBOSITY,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(
                    f"{Const.ROOT_DIR}/data/log"
                    ),
                logging.StreamHandler()
                ],
            )

        if lvl == 10:
            debug(msg)
        elif lvl == 20:
            info(msg)
        elif lvl == 30:
            warning(msg)
        elif lvl == 40:
            error(msg)
        elif lvl == 50:
            critical(msg)

