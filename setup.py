"""
AUTHOR: Artur Barseghyan
    (artur.barseghyan@gmail.com)
DESCRIPTION
    Additional XML sitemap functionality for Django.
"""

import os
from setuptools import setup, find_packages

readme = open(os.path.join(os.path.dirname(__file__), 'readme.txt')).read()

version = '0.2'

setup(
    name='qartez',
    version=version,
    description=("Additional XML sitemap functionality for Django"),
    long_description = readme,
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='xml sitemaps, django, app, python',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://bitbucket.org/barseghyanartur/qartez',
    package_dir={'':'src'},
    packages=find_packages(where='./src'),
)