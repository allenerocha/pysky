"""Module to output the list of visible objects to various formats."""
from .html_list import HTML_list
from .const import Const
from datetime import datetime


def to_html_list(items: list, filename: str) -> None:
    html_list = HTML_list(items)
    with open(
            f"{Const.SLIDESHOW_DIR}"
            f"/PySkySlideshow/{filename}.html",
            "w"
    ) as out_file:
        out_file.write(html_list.__str__())

