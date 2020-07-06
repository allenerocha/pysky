"""Module to output the list of visible objects to various formats."""
from datetime import datetime

from .const import Const
from .html_list import HTML_list
from .html_table import HTML_table


def to_html_list(items: list, filename: str) -> None:
    html_list = HTML_list(items, delimiter=",")
    with open(
            f"{Const.SLIDESHOW_DIR}"
            f"/PySkySlideshow/{filename}.html",
            "w"
    ) as out_file:
        out_file.write(html_list.__str__())

def to_html_table(items: list, filename=''):
    html_table = HTML_table()
    html_table.add_header(items[0])
    for item in items:
        html_table.add_row(item)
    html_table.dump(filename)
