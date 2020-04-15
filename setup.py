from setuptools import setup

setup(
        name='pysky',
        version='0.1',
        packages=find_packages(),
        install_requires=[
            'json',
            'os',
            'sys',
            'time',
            'astropy == 4.0',
            'astroquery == 0.4',
            'astroplan == 0.6',
            'logging',
            'datetime',
            'base64',
            'Pillow >= 6.2.2',
            'io',
            'urllib',
            'requests == 2.21.0',
            'beautifulsoup4 == 4.8.2'
            ],
        entry_points={
            "console_scripts": [
                pysky=pysky:main
                ]
            },
        author="Allen Rocha",
        author_email="allenerocha@pm.me",
        description="This is an application to view what will be visible in the sky in a given a time range.",
        url="http://github.com/allenerocha/PySky",
        project_urls={
            "Source Code": "https://github.com/allenerocha/PySky",
            },
        )
