"""Module to output the list of visible objects to various formats."""

from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
from astroplan import Observer
from astroplan.plots import plot_sky
from astropy.time import Time
from numpy import linspace

from .const import Const
from .html_list import HTML_list
from .html_table import HTML_table
from .logger import Logger


def to_html_list(items: list, filename: str) -> None:
    html_list = HTML_list(items, delimiter=",")
    with open(
        Path(Const.SLIDESHOW_DIR, "PySkySlideshow", f"{filename}.html"), "w"
    ) as out_file:
        out_file.write(html_list.__str__())


def to_html_table(items: list, filename=""):
    html_table = HTML_table()
    html_table.add_header(items[0])
    for item in items:
        html_table.add_row(item)
    html_table.dump(filename)


def generate_plot(celestial_obj):
    """
    Generate the plot of the given target.

    :param celestial_obj: FixedTarget object to find.
    """
    
    Logger.log(f"Generating plot for {celestial_obj.name}")
    plt.figure(figsize=(8, 6))
    location = Observer(
        longitude=Const.LATITUDE * u.deg,
        latitude=Const.LONGITUDE * u.deg,
        elevation=Const.ELEVATION * u.m,
        name="location",
        timezone="UTC",
    )
    start_time = Time(
        f"{Const.START_YEAR}-{Const.START_MONTH}-{Const.START_DAY} {Const.START_TIME}"
    )
    end_time = Time(
        f"{Const.END_YEAR}-{Const.END_MONTH}-{Const.END_DAY} {Const.END_TIME}"
    )
    delta_t = end_time - start_time
    linspace_count = int(delta_t.to_value("min") / 15)
    time_range = start_time + delta_t * linspace(0, 1, linspace_count)
    plot_sky(celestial_obj, location, time_range)
    plt.legend(loc="lower left", bbox_to_anchor=(0.85, 0.0))
    plt.savefig(
        Path(
            Const.SLIDESHOW_DIR,
            "PySkySlideshow",
            "plots",
            f"{str(celestial_obj.name).replace(' ', '')}_{Const.START_YEAR}-{Const.START_MONTH}-{Const.START_DAY}.pdf",
        ),
        dpi=300,
        format="pdf",
    )
    Logger.log(
        f"Plot for {celestial_obj.name} generated at {Path(Const.SLIDESHOW_DIR,'PySkySlideshow','plots')}"
    )
    plt.clf()
    plt.cla()
    plt.close('all')
