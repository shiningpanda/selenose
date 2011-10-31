.. SeleniumServer documentation master file, created by
   sphinx-quickstart on Sat Oct 29 16:20:54 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SeleniumServer
==============

SeleniumServer is a plugin for `nose <http://code.google.com/p/python-nose/>`_ developed by `ShiningPanda <https://www.shiningpanda.com>`_. This plugin starts a `Selenium Server <http://seleniumhq.org/docs/05_selenium_rc.html#selenium-server>`_ before running tests, and stops it at the end of the tests.

Installation
------------

On most UNIX-like systems, you’ll probably need to run these commands as root or using ``sudo``.

Install `Selenium Server <http://seleniumhq.org/docs/05_selenium_rc.html#selenium-server>`_ using `setuptools <http://pypi.python.org/pypi/setuptools/>`_/`distribute <http://pypi.python.org/pypi/distribute/>`_:

::

    easy_install SeleniumServer
    
Or `pip <http://pypi.python.org/pypi/pip/>`_:

::

    pip install SeleniumServer

It can take time as `Selenium Server <http://seleniumhq.org/docs/05_selenium_rc.html#selenium-server>`_'s jar is downloaded during installation.

Configuration
-------------

To enable this plugin, add ``--with-selenium-server`` on the nose command line:

::

    nose --with-selenium-server

You can also add the ``with-selenium-server`` option under the ``nosetests`` section in a configuration file (``setup.cfg``, ``~/.noserc`` or ``~/nose.cfg``):

::

    [nosetests]
    with-selenium-server = true

`Selenium Server <http://seleniumhq.org/docs/05_selenium_rc.html#selenium-server>`_'s options can be found by typing:

::

    java -jar /path/to/seleniumserver/libs/selenium-server-standalone-X.X.X.jar -h
    
To set server options, add a ``selenium-server`` section in a configuration file (``setup.cfg``, ``~/.noserc`` or ``~/nose.cfg``). Option names are obtained by removing the initial dash, for instance to run:

::

    java -jar selenium-server-standalone-X.X.X.jar -debug -log selenium-server.log 

Add following options in configuration:

::

    [selenium-server]
    debug = true
    log = selenium-server.log


Write tests
-----------

When writing tests, it's convenient to start a `Selenium Server <http://seleniumhq.org/docs/05_selenium_rc.html#selenium-server>`_ manually. To do so, execute:

::

    $ selenium-server
    Starting... done!

    Quit the server with CONTROL-C.

Then type ``CONTROL-C`` or ``CTRL-BREAK`` to stop the server.
