#!/usr/bin/env python3

"""The setup script."""

from setuptools import setup

import pysky

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "alabaster==0.7.12",
    "appdirs==1.4.4",
    "argh==0.26.2",
    "astroplan==0.6",
    "astropy==4.0",
    "astroquery==0.4.1",
    "Babel==2.8.0",
    "beautifulsoup4==4.8.2",
    "black==20.8b1",
    "bleach==3.1.5",
    "bump2version==0.5.11",
    "certifi==2020.4.5.2",
    "cffi==1.14.0",
    "chardet==3.0.4",
    "click==7.1.2",
    "codecov==2.1.9",
    "colorama==0.4.3",
    "coverage==4.5.4",
    "cryptography>=3.2",
    "distlib==0.3.0",
    "docutils==0.16",
    "entrypoints==0.3",
    "filelock==3.0.12",
    "flake8==3.7.8",
    "html5lib==1.0.1",
    "idna==2.8",
    "imagesize==1.2.0",
    "jeepney==0.4.3",
    "jplephem==2.15",
    "Jinja2==2.11.2",
    "keyring==21.2.1",
    "MarkupSafe==1.1.1",
    "mccabe==0.6.1",
    "mypy-extensions==0.4.3",
    "numpy==1.18.5",
    "packaging==20.4",
    "pathspec==0.8.0",
    "pathtools==0.1.2",
    "Pillow==7.1.2",
    "pkginfo==1.5.0.1",
    "pluggy==0.13.1",
    "py>=1.10.0",
    "pycodestyle==2.5.0",
    "pycparser==2.20",
    "pyflakes==2.1.1",
    "Pygments>=2.7.4",
    "pyparsing==2.4.7",
    "pytz==2020.1",
    "pywin32-ctypes==0.2.0",
    "PyYAML==5.3.1",
    "readme-renderer==26.0",
    "regex==2020.7.14",
    "requests==2.21.0",
    "requests-toolbelt==0.9.1",
    "SecretStorage==3.1.2",
    "six==1.15.0",
    "snowballstemmer==2.0.0",
    "soupsieve==2.0.1",
    "Sphinx==1.8.5",
    "sphinxcontrib-websupport==1.2.2",
    "toml==0.10.1",
    "tox==3.14.0",
    "tox-travis==0.12",
    "tqdm==4.46.1",
    "twine==1.14.0",
    "typed-ast==1.4.1",
    "typing-extensions==3.7.4.3",
    "urllib3==1.24.3",
    "virtualenv==20.0.21",
    "watchdog==0.9.0",
    "webencodings==0.5.1",
    "matplotlib<3.3",
    "setuptools~=47.1.0",
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
    url=pysky.__url__,
    project_urls={
        "Source Code": pysky.__url__,
    },
    version=pysky.__version__,
)
