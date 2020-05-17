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

   $ pysky -sd 2012-10-07 -st 17:00 -ed 2012-10-07 -et 23:00

Start December 31st, 2015 08:00 End January 1st, 2016 02:00 with high verbosity
-------------------------------------------------------------------------------


 .. code-block:: bash

   $ pysky -sd 2015-31-12 -st 08:00 -ed 2016-01-01 -et 02:00 -v 5

Start September 1st, 2019 19:00 for one hour with 2 threads and medium verbosity
--------------------------------------------------------------------------------


 .. code-block:: bash

   $ pysky -sd 2019-01-09 -st 17:00 -t 2 -v 3

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

