Pysky
=====

.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat
    :alt: AstroPy
    :target: https://www.astropy.org/
.. image:: https://travis-ci.org/allenerocha/pysky.svg?branch=master
    :alt: Travis (.org)
    :target: https://travis-ci.org/allenerocha/pysky
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: black
    :target: https://github.com/psf/black
.. image:: https://codecov.io/gh/allenerocha/pysky/branch/master/graph/badge.svg
    :alt: Codecov
    :target: https://codecov.io/gh/allenerocha/pysky
.. image:: https://img.shields.io/badge/license-AGPLv3-green
     :alt: License:AGPLv3
    :target: https://www.gnu.org/licenses/agpl-3.0.en.html
.. image:: https://img.shields.io/github/last-commit/allenerocha/pysky
    :alt: GitHub last commit
    :target: https://www.github.com/allenerocha/pysky/commits/master

Download & Installation
=======================

Initial setup
-------------
Download and install latest version of Python `here`_.

.. _here: https://www.python.org/downloads/

Follow `these`_ instructions to get the latest version of pip.

.. _these: https://pip.pypa.io/en/stable/installing/



 .. code-block:: bash

    ~$ git clone https://github.com/allenerocha/pysky.git && cd pysky/

 .. code-block:: bash

    pysky/$ pip install .


Uninstalling
============

 .. code-block:: bash

   ~$ pip uninstall pysky -y


Usage
=====

 .. code-block:: bash

   ~$ pysky -sd [start date] -st [start time] -ed [end date] -et [end time] -t [thread count] -v [verbosity level]

Command line options
--------------------
Options (Dates and times are in `ISO 8601`_ format)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
===================  =================
``-sd/--startdate``  Starting date. [#f1]_
``-st/--starttime``  Starting time. [#f1]_
``-ed/--enddate``    Ending date. [#f2]_
``-et/--endtime``    Ending time. [#f2]_
``-t/--threads``     Number of threads
                     to use. [#f2]_
``-v/--verbosity``   Verbosity level. [#f2]_
``-h/--help``        Display help for
                     the CL options.
===================  =================

.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
.. [#f1] Required.
.. [#f2] Optional.

Date format (YEAR-MONTH-DAY)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
=========   ==============
``YEAR``    4 digit format
``MONTH``   2 digit format
``DAY``     2 digit format
=========   ==============

Time format (HOUR:MINUTE)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
==========   =====================
``HOUR``     24 hour format (0-23)
``MINUTE``   Minute in regular
             format (0-59)
==========   =====================

Specifying no end date and time defaults the search to only go for one hour long.

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

   $ pysky -sd 2012-07-10 -st 17:00 -ed 2012-07-10 -et 23:00

Start December 31st, 2015 08:00 End January 1st, 2016 02:00 with high verbosity
-------------------------------------------------------------------------------


 .. code-block:: bash

   $ pysky -sd 2015-12-31 -st 08:00 -ed 2016-01-01 -et 02:00 -v 5

Start September 1st, 2019 19:00 for one hour with 2 threads and medium verbosity
--------------------------------------------------------------------------------


 .. code-block:: bash

   $ pysky -sd 2019-09-01 -st 17:00 -t 2 -v 3

Supported Python Versions
=========================

    Python 3.6+
