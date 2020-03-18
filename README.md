PySky

# Usage

    ./pysky.py [start date (string)] [start time (string)] [end date (string)] [end time (string)]

# Images
    By default images of valid objects will be saved in the filename format:
        object-width-height-resolution-scaling-creationdate.png

## Date format

    Date (YEAR-DAY-MONTH)
        YEAR                Year in 4 digit format
        DAY                 Day in 2 digit format
        MONTH               Month in 2 digit format

## Time format

    Time (HOUR:MINUTE)
        HOUR                24 hour format (0-23)
        MINUTE              Minute in regular format (0-59)

### Examples

#### Start July 10th, 2012 17:00 End July 10th, 2012 23:00
    ./pysky.py 2012-10-07 17:00 2012-10-07 23:00

#### Start December 31st, 2015 08:00 End January 1st, 2016 02:00
    ./pysky.py 2015-31-12 08:00 2016-01-01 02:00

# Supported Python Versions

    Python 3.x

# Dependencies

- [astropy](https://github.com/astropy/astropy)
- [astroquery](https://github.com/cds-astro/astroquery)
- [html5lib](https://github.com/html5lib/html5lib-python)
- [Beautiful Soup 4 (bs4)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [requests](https://requests.readthedocs.io/en/master/)
- [Pillow](https://python-pillow.org/)
