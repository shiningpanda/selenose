# -*- coding: utf-8 -*-
import os
import sys

folder = os.path.dirname(os.path.abspath(__file__))

exec(open(os.path.join(folder, 'selenose', '__init__.py')).read())

onsite = os.path.exists(os.path.join(folder, 'PKG-INFO'))

from selenose import libs

flag = '--include'
include = ( flag in sys.argv )
if include:
    sys.argv.remove(flag)

if not onsite and not include and 'bdist_egg' in sys.argv:
    print >> sys.stderr, 'bdist_egg is no available, can not embed jar in .egg for license reasons...'
    sys.exit(1)

if not include and 'sdist' in sys.argv:
    libs.clean(__version__, full=True)
else:
    libs.clean(__version__)
    libs.download(__version__)

try: import setuptools
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = 'selenose',
    version = __version__,
    description = 'Selenium plugin for nose',
    long_description = 'Selenium plugin for nose/nosetests.',
    url = 'https://github.com/shiningpanda/selenose/',
    download_url = 'http://pypi.python.org/pypi/selenose/',
    license = 'GNU Affero General Public License',
    author = 'ShiningPanda',
    author_email = 'developers@shiningpanda.com',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
    install_requires = [
        'nose >= 1.1.2',
        'selenium >= %s' % __version__
    ],
    entry_points = {
        'nose.plugins.0.10': [
            'selenium-server = selenose.plugins:SeleniumServerPlugin',
            'selenium-driver = selenose.plugins:SeleniumDriverPlugin',
        ],
        'console_scripts': [
            'selenium-server = selenose.server:_run',
        ],
    },
    test_suite = 'nose.collector',
)
