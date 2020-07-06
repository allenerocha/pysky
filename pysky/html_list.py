"""HTML class that contains functions to transform inputs to an HTML compliant format."""


class HTML_list:
    def __init__(self, html_list=None, delimiter=" "):
        self.delimiter = delimiter
        if html_list is None:
            self.html_list = list()
        else:
            self.html_list = html_list

    def append(self, item) -> None:
        """Append item(s) to the html list."""
        self.html_list.append(item)

    def __str__(self) -> str:
        out = str()
        for index, item in enumerate(self.html_list):
            if index == 0:
                out += "<ol>\n"
            for celestial_obj, propteries in item.items():
                out += "<li>"
                out += (
                    "<span style='font-weight: 400;'>"
                    + f"{celestial_obj}"
                    + self.delimiter
                    + "</span>"
                )
                jndex = 0
                for key, value in propteries.items():
                    if " (petameters)" in str(key).lower():
                        key = str(key).lower().replace(" (petameters)", "").title()
                        value = "{:,.2f}".format(value) + " Pm"
                    out += (
                        "<span style='font-weight: 400;'>"
                        + f"{key.title()}: {str(value).title()}"
                    )
                    if jndex != (len(propteries) - 1):
                        out += self.delimiter
                    out += "</span>"
                    jndex += 1
                out += "</li>\n"
            if index == (len(self.html_list) - 1):
                out += "</ol>\n"
        return out
