PySky

# Usage
    ./__main__.py for usage help
    ./__main__.py [start date (string)] [start time (string)] [end date (string)] [end time (string)]

# Images
    By default images of valid objects will be saved in the filename format:
        slideshow/object-width-height-resolution-scaling-creationdate.png

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
    ./__main__.py 2012-10-07 17:00 2012-10-07 23:00

#### Start December 31st, 2015 08:00 End January 1st, 2016 02:00
    ./__main__.py 2015-31-12 08:00 2016-01-01 02:00

# Supported Python Versions

    Python 3.6+

# Dependencies

- [astropy == 4.0](https://github.com/astropy/astropy)
- [astroplan == 0.6](https://astroplan.readthedocs.io/)
- [astroquery == 0.4](https://github.com/cds-astro/astroquery)
- [beautifulsoup4 == 4.8.2](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [requests == 2.21.0](https://requests.readthedocs.io/en/master/)
- [Pillow >= 6.2.2](https://python-pillow.org/)
