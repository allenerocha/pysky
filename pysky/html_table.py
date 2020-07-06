"""HTML class that contains functions to transform inputs to an HTML compliant format."""
from typing import Dict, List

from .const import Const


class HTML_table:
    def __init__(self, delimiter='|'):
        """
        Initialize the table properties.

        Calling sequence:
            html_table = HTML_table()
        :param delimiter: Delimiter to seperate the items.
        """
        self.delimiter = delimiter
        self.header = ['Name']
        self.rows: List[list] = list()

    def add_header(self, star: dict):
        """
        Add the header file to the CSV file.

        Calling sequence:
            html_table.add_header(['Type', 'Alt.', 'Az.'])
        :param titles: List of titles to add to the header line.
        """
        for _, attribute in star.items():
            for title in attribute.keys():
                self.header.append(title)

    def add_row(self, row: dict):
        """
        Add a row csv file.

        Calling sequence:
            html_table.add_row('NGC 5139': {
                'Type': 'Globular Cluster', 'Alt.': 28.67, 'Az.': 212.93
            })
        :param row: Dictionary row to add to the row.
        """
        name_col = list(row.keys())[0]
        cols = list(row[name_col].values())
        cols.insert(0, name_col)
        self.rows.append(cols)

    def dump(self, filename=''):
        """
        Write the CSV file with the given filename.

        Calling sequence:
            html_table.dump()
        :param filename:    File name for the CSV output. By default, it will
                            generate it with the name
                            `pysky-report-YEAR-MON-DAY` where YEAR-MON-DAY
                            is the starting date argument given.
        """
        if filename == '' or not isinstance(filename, str):
            filename = 'pysky-report-' +\
                    f'{Const.START_YEAR}-{Const.START_MONTH}-{Const.START_DAY}'
        with open(
                f'{Const.SLIDESHOW_DIR}/PySkySlideshow/{filename}.html', 'w'
                ) as html_out:
            html_out.write("<table>\n")
            html_out.write("<caption>")
            html_out.write(
                f"{Const.START_YEAR}-{Const.START_MONTH}-{Const.START_DAY}"
            )
            html_out.write("</caption>\n")
            html_out.write("<thead>\n")
            html_out.write("<tr>")
            for title in self.header:
                html_out.write(f"<td>{str(title).title()}</td>\n")
            html_out.write("</tr>\n")
            html_out.write("</thead>\n")

            html_out.write("<tbody>\n")
            for row in self.rows:
                html_out.write("<tr>\n")
                for index, element in enumerate(row):
                    # if index < (len(row) - 1):
                    html_out.write(f"<td>{str(element)}</td>\n")
                html_out.write("</tr>\n")
            html_out.write("</tbody>\n")
            html_out.write("</table>\n")
