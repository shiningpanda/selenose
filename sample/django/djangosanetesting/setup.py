# -*- coding: utf-8 -*-
import os
import sys

import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages

if 'nosetests' in sys.argv:
    basedir = os.path.dirname(os.path.abspath(__file__))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    sys.path.insert(0, basedir)
    sys.path.insert(0, os.path.join(basedir, 'djangotutorial'))

setup(
    name = 'DjangoTutorial',
    version = '1.3.1',
    description = 'Django tutorial.',
    url = 'https://docs.djangoproject.com/en/1.3/intro/tutorial01/',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'Django >= 1.3.1',
    ],
    setup_requires = [
        'SeleniumServer',
        'djangosanetesting >= 0.5.11',
        'CherryPy',
    ]
)
