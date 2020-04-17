#!/usr/bin/env python3

"""The setup script."""

from setuptools import find_packages, setup

import pysky

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "astropy == 4.0",
    "astroquery == 0.4",
    "astroplan == 0.6",
    "Pillow >= 6.2.2",
    "requests == 2.21.0",
    "beautifulsoup4 == 4.8.2",
]

packages = ["pysky"]

setup_requirements = []

test_requirements = []

setup(
    author=pysky.__author__,
    author_email=pysky.__email__,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    description=pysky.__description__,
    entry_points={"console_scripts": ["pysky = pysky.__main__:main"]},
    install_requires=requirements,
    license=pysky.__licence__,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="pysky",
    name=pysky.__title__,
    packages=packages,
    package_dir={"pysky": "pysky"},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="http://github.com/allenerocha/PySky",
    project_urls={"Source Code": "https://github.com/allenerocha/PySky",},
    version=pysky.__version__,
)
