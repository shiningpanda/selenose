# -*- coding: utf-8 -*-
import os
import sys
import codecs

# Check if SETUPTOOLS is available. If not available, use setup script
try: import setuptools
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()

from setuptools import setup, find_packages

from seleniumserver import libs

version = '2.14.0'

folder = os.path.dirname(os.path.abspath(__file__))

onsite = os.path.exists(os.path.join(folder, 'PKG-INFO'))

if not onsite:
    fd = codecs.open(os.path.join(folder, 'seleniumserver', '__version__.py'), 'w', 'utf-8')
    fd.write("""#-*- coding: utf-8 -*-
__version__ = %s
""" % repr(version))

flag = '--include'
include = ( flag in sys.argv )
if include:
    sys.argv.remove(flag)

if not onsite and not include and 'bdist_egg' in sys.argv:
    print >> sys.stderr, 'bdist_egg is no available, can not embed jar in .egg for license reasons...'
    sys.exit(1)

if not include and 'sdist' in sys.argv:
    libs.clean(version, full=True)
else:
    libs.clean(version)
    libs.download(version)

setup(
    name = 'SeleniumServer',
    version = version,
    description = 'Selenium server plugin for Nose',
    long_description = 'A plugin for nose/nosetests to start a Selenium server before running tests.',
    url = 'https://github.com/shiningpanda/seleniumserver/',
    download_url = 'http://pypi.python.org/pypi/seleniumserver/',
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
        'pexpect >= 2.4',
        'selenium >= %s' % version
    ],
    entry_points = {
        'nose.plugins.0.10': [
            'selenium-server = seleniumserver.plugins:SeleniumServerPlugin',
            'selenium-driver = seleniumserver.plugins:SeleniumDriverPlugin',
        ],
        'console_scripts': [
            'selenium-server = seleniumserver.server:_run',
        ],
    },
    test_suite = 'nose.collector',
)
