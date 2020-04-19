PySky
=====

Download & Installation
=======================

 .. code-block:: bash

    ~$ git clone https://github.com/allenerocha/pysky.git && cd pysky/

 .. code-block:: bash

    pysky/$ pip3 install .


Uninstalling
============

 .. code-block:: bash

   ~$ pip3 uninstall pysky -y


Usage
=====

 .. code-block:: bash

   ~$ pysky [start date] [start time] [end date] [end time]

Command line options
--------------------
Date format (YEAR-DAY-MONTH)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
=========   ==============
``YEAR``    4 digit format
``DAY``     2 digit format
``MONTH``   2 digit format
=========   ==============

Time format (HOUR:MINUTE)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
==========   =====================
``HOUR``     24 hour format (0-23)
``MINUTE``   Minute in regular
             format (0-59)
==========   =====================

Help
----

``~$ pysky``

--------------

Images
======

By default images of valid objects will be saved in the filename format:

``$HOME/PySkySlideshow/object-width-height-resolution-scaling.png``

Examples
========


Start July 10th, 2012 17:00 End July 10th, 2012 23:00
-----------------------------------------------------


 .. code-block:: bash

   $ pysky 2012-10-07 17:00 2012-10-07 23:00

Start December 31st, 2015 08:00 End January 1st, 2016 02:00
-----------------------------------------------------------


 .. code-block:: bash

   $ pysky 2015-31-12 08:00 2016-01-01 02:00``

Supported Python Versions
=========================

    Python 3.6+

Dependencies
============

-  `astropy == 4.0 <https://github.com/astropy/astropy>`__
-  `astroplan == 0.6 <https://astroplan.readthedocs.io/>`__
-  `astroquery == 0.4 <https://github.com/cds-astro/astroquery>`__
-  `beautifulsoup4 ==
   4.8.2 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`__
-  `requests == 2.21.0 <https://requests.readthedocs.io/en/master/>`__
-  `Pillow >= 6.2.2 <https://python-pillow.org/>`__

