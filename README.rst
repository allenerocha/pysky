PySky
=====

.. image:: https://img.shields.io/travis/allenerocha/pysky
    :alt: Travis (.org)
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: black https://github.com/psf/black
.. image:: https://img.shields.io/codecov/c/github/allenerocha/pysky
    :alt: Codecov
.. image:: https://img.shields.io/badge/license-AGPLv3-green
     :alt: License:AGPLv3

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

   ~$ pysky [start date] [start time] [end date] [end time] [thread count] [verbosity level]

Command line options
--------------------
Options
^^^^^^^
===================  =================
``-sd/--startdate``  Starting date.
``-st/--starttime``  Starting time.
``-ed/--enddate``    Ending date.
``-et/--endtime``    Ending time.
``-t/--threads``     Number of threads
                     to use.
``-v/--verbosity``   Verbosity level.
``-h/--help``        Display help for
                     the CL options.
===================  =================

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
 .. code-block:: bash

   ~$ pysky -h

 .. code-block:: bash

   ~$ pysky --help

--------------

Images
======
Default
-------
By default images of valid objects will be saved in the filename format:

``$HOME/PySkySlideshow/object-width-height-resolution-scaling.png``

User Defined
------------
To change the location of the saved images, you can add the following line to the ``user_prefs.cfg`` file:

``slideshow_dir=``

Followed by the directory to save in. The folder PySkySlideshow will be created in the specified directory.

Examples
^^^^^^^^
``slideshow_dir=/home/allen``

This will set the directory to save the images as:

``slideshow_dir=/home/allen/PySkySlideshow/``


Usage
=====


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

