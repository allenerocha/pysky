"""HTML class that contains functions to transform inputs to an HTML compliant format."""


class HTML_list:
    def __init__(self, html_list=None):
        if html_list is None:
            self.html_list = list()
        else:
            self.html_list = html_list

    def append(self, item) -> None:
        """Append item(s) to the html list"""
        self.html_list.append(item)

    def __str__(self) -> str:
        out = str()
        for index, item in enumerate(self.html_list):
            if index == 0:
                out += "<ol>\n"
            elif index == (len(self.html_list) - 1):
                out += "</ol>\n"
                break

            out += "<li>" + \
                   "<span style='font-weight: 400;'>" + \
                   f"{item['name']} " + \
                   "</span>" + \
                   "<span style='font-weight: 400;'>" + \
                   f"{item['constellation']} " + \
                   "</span>" + \
                   "<span style='font-weight: 400;'>" + \
                   f"{item['type']} " + \
                   "</span>" + \
                   "<span style='font-weight: 400;'>" + \
                   f"{item['brightness']} " + \
                   "</span>" + \
                   "<span style='font-weight: 400;'>" + \
                   f"{item['distance']} " + \
                   "petameters." + \
                   "</span>" + \
                   "</li>\n"
        return out
