"""Module to output the list of visible objects tp various formats"""
from .html_list import HTML_list
from .const import Const


def to_html_list(items: list) -> None:
    html_list = HTML_list(items)
    with open(
            f"/home/allen"
            f"/PySkySlideshow/visible_stars_output.html",
            "w"
    ) as out_file:
        out_file.write(html_list.__str__())
