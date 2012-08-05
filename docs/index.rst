.. selenose documentation master file, created by
   sphinx-quickstart on Sat Oct 29 16:20:54 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Selenose
========

Selenose provides a set of `Selenium <http://seleniumhq.org/>`_ related plugins/tasks for `nose <http://code.google.com/p/python-nose/>`_/`django-jenkins <http://pypi.python.org/pypi/django-jenkins/>`_ developed by `ShiningPanda <https://www.shiningpanda.com>`_.

The use of these plugins/tasks is detailed bellow, but let's have a look on the :ref:`installation process <installation>` first.

.. _installation:

Installation
------------

On most UNIX-like systems, you’ll probably need to run these commands as root or using ``sudo``.

Install selenose using `setuptools <http://pypi.python.org/pypi/setuptools/>`_/`distribute <http://pypi.python.org/pypi/distribute/>`_:

.. code-block:: bash

    $ easy_install selenose
    
Or `pip <http://pypi.python.org/pypi/pip/>`_:

.. code-block:: bash

    $ pip install selenose

It can take a while as Selenium server's jar is downloaded on the fly during installation.

If you plan to use `django-jenkins <http://pypi.python.org/pypi/django-jenkins/>`_, note that Django 1.4+ is required (`support for in-browser testing frameworks <https://docs.djangoproject.com/en/dev/releases/1.4/#support-for-in-browser-testing-frameworks>`_).

Nose
----

Selenose provides two `Selenium <http://seleniumhq.org/>`_ related plugins for `nose <http://code.google.com/p/python-nose/>`_:

* :ref:`selenium-server-plugin` starts a `Selenium Server <http://seleniumhq.org/docs/05_selenium_rc.html#selenium-server>`_ before running tests, and stops it at the end of the tests.
* :ref:`selenium-driver-plugin` provides a `Selenium Web Driver <http://seleniumhq.org/docs/03_webdriver.html>`_ to the tests.

.. _selenium-server-plugin:

Selenium Server Plugin
^^^^^^^^^^^^^^^^^^^^^^

This plugin starts a Selenium Server before running tests, and stops it at the end of the tests.

To enable it, add ``--with-selenium-server`` to the nose command line:

.. code-block:: bash

    $ nose --with-selenium-server

You can also add the ``with-selenium-server`` option under the ``nosetests`` section of the configuration file (``setup.cfg``, ``~/.noserc`` or ``~/nose.cfg``):

.. code-block:: cfg

    [nosetests]
    with-selenium-server = true

Options for Selenium Server can be found by `downloading its jar <http://seleniumhq.org/download/>`_ and typing:

.. code-block:: bash

    $ java -jar /path/to/seleniumserver/libs/selenium-server-standalone-X.X.X.jar -h
   

Most common options are:

* ``-port <nnnn>``: the port number the Selenium Server should use (default 4444),
* ``-log <logFileName>``: writes lots of debug information out to a log file,
* ``-debug``: enable debug mode.

To set the server options, add a ``selenium-server`` section to the configuration file (``setup.cfg``, ``~/.noserc`` or ``~/nose.cfg``).
Option names are obtained by removing the initial dash, for instance to run:

.. code-block:: bash

    $ java -jar selenium-server-standalone-X.X.X.jar -debug -log selenium-server.log 

Add the following options to the configuration:

.. code-block:: cfg

    [selenium-server]
    debug = true
    log = selenium-server.log

In your test, just create a new ``Remote`` Web Driver calling the server and that's it:

.. code-block:: python

    import nose
    import unittest

    from selenium import webdriver

    class TestCase(unittest.TestCase):
    
        def test(self):
            driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
            try:
                driver.get('http://www.google.com')
                # Your test here...
            finally:
                driver.quit()
         
    if __name__ == '__main__':
        nose.main()

.. _selenium-driver-plugin:

Selenium Driver Plugin
^^^^^^^^^^^^^^^^^^^^^^

This plugin provides a Selenium Web Driver to Selenium tests.

Flag Selenium tests
+++++++++++++++++++

This plugin only provides Web Drivers to Selenium test. To declare a Selenium test:

* Either make your test case inherit from ``selenose.cases.SeleniumTestCase``,
* Or set a ``enable_selenium_driver`` flag to ``True``:

.. code-block:: python

    class TestCase(unittest.TestCase):
        enable_selenium_driver = True

Enable the plugin
+++++++++++++++++

To enable this plugin, add ``--with-selenium-driver`` on the nose command line:

.. code-block:: bash

    $ nose --with-selenium-driver

You can also add the ``with-selenium-driver`` option under the ``nosetests`` section to the configuration file (``setup.cfg``, ``~/.noserc`` or ``~/nose.cfg``):

.. code-block:: cfg

    [nosetests]
    with-selenium-driver = true

But enabling it is not enough, a :ref:`web-driver-environment` is also required.

.. _web-driver-environment:

Web Driver environment
++++++++++++++++++++++

An environment declares all the necessary parameters to create a new Web Driver.

To create a new environment ``sample``, add a ``selenium-driver:sample`` section to the configuration file (``setup.cfg``, ``~/.noserc`` or ``~/nose.cfg``) with at least a ``webdriver`` option:

.. code-block:: cfg

    [selenium-driver:sample]
    webdriver = firefox

This ``webdriver`` option defines the Web Driver to use. Here are the available values:

* ``chrome`` for `Chrome <https://www.google.com/chrome>`_, allowing the following options in configuration:
    * ``executable_path`` (optional): path to ``chromedriver`` executable,
    * ``port`` (optional),
    * ``desired_capabilities`` (optional), 
* ``firefox`` for `Firefox <http://www.mozilla.org/firefox/>`_, allowing the following options in configuration:
    * ``timeout`` (optional),
* ``ie`` for `Internet Explorer <http://windows.microsoft.com/en-US/internet-explorer/products/ie/home>`_, allowing the following options in configuration:
    * ``port`` (optional),
    * ``timeout`` (optional),
* ``remote`` to delegate to a Selenium Server (started by :ref:`selenium-server-plugin`?), allowing the following options in configuration:
    * ``command_executor`` (required): url of the server (``http://127.0.0.1:4444/wd/hub`` by default),
    * ``desired_capabilities (required): the desired browser, it could be the lower case field name of ``selenium.webdriver.DesiredCapabilities`` such as ``firefox``, ``htmlunitwithjs``... or a comma separated key/value list such as ``browserName=firefox,platform=ANY``.

To enable an environment, add ``--selenium-driver`` on the nose command line:

.. code-block:: bash

    $ nose --with-selenium-driver --selenium-driver=sample

You can also add the ``selenium-driver`` option under the ``nosetests`` section to the configuration file (``setup.cfg``, ``~/.noserc`` or ``~/nose.cfg``):

.. code-block:: cfg

    [nosetests]
    with-selenium-driver = true
    selenium-driver = sample

    [selenium-driver:sample]
    webdriver = firefox

Selenose also provides a set of predefined but overridable environments:

.. code-block:: cfg

    [selenium-driver:chrome]
    webdriver = chrome

    [selenium-driver:ie]
    webdriver = ie

    [selenium-driver:firefox]
    webdriver = firefox

    [selenium-driver:remote-htmlunit]
    webdriver = remote
    desired_capabilities = htmlunit
    
    [selenium-driver:remote-htmlunitwithjs]
    webdriver = remote
    desired_capabilities = htmlunitwithjs
    
    [selenium-driver:remote-opera]
    webdriver = remote
    desired_capabilities = opera

    [selenium-driver:remote-...]
    webdriver = remote
    desired_capabilities = ...

Writing tests
+++++++++++++

The Web Driver is directly available with ``self.driver`` and there is no need to cleanup after use, selenose will do it for you:

.. code-block:: python

    import nose
    
    from selenose.cases import SeleniumTestCase
    
    class TestCase(SeleniumTestCase):
        
        def test(self):
            self.driver.get('http://www.google.com')
            # Your test here...

    if __name__ == '__main__':
        nose.main()

Combining Server & Driver
^^^^^^^^^^^^^^^^^^^^^^^^^

To combine a Selenium Server and a Selenium Driver plugin, just enable them both: the ``command_executor`` option of the ``remote`` Web Driver will know the correct value to reach the Selenium Server.

Django Jenkins
--------------

Selenose provides two `Selenium <http://seleniumhq.org/>`_ related tasks for `django-jenkins <http://pypi.python.org/pypi/django-jenkins/>`_:

* :ref:`selenium-server-task` starts a `Selenium Server <http://seleniumhq.org/docs/05_selenium_rc.html#selenium-server>`_ before running tests, and stops it at the end of the tests.
* :ref:`selenium-driver-task` provides a `Selenium Web Driver <http://seleniumhq.org/docs/03_webdriver.html>`_ to the tests.

Note that Django 1.4+ `support for in-browser testing frameworks <https://docs.djangoproject.com/en/dev/releases/1.4/#support-for-in-browser-testing-frameworks>`_ is required.

.. _selenium-server-task:

Selenium Server Task
^^^^^^^^^^^^^^^^^^^^

This task starts a Selenium Server before running tests, and stops it at the end of the tests.

To enable it, edit your ``settings.py`` and append ``selenose.tasks.selenium_server`` to ``JENKINS_TASKS``:

.. code:: python
    
    JENKINS_TASKS = [
        # Other tasks...
        'selenose.tasks.selenium_server',
    ]

If this setting does not exist yet, do not forget to create it with the default tasks:

.. code:: python
    
    JENKINS_TASKS = [
        'django_jenkins.tasks.run_pylint',
        'django_jenkins.tasks.with_coverage',
        'django_jenkins.tasks.django_tests',
        'selenose.tasks.selenium_server',
    ]

Options for Selenium Server are the same than for the nose :ref:`selenium-server-plugin`.
Set them in a ``setup.cfg`` located in the current working directory, for instance:

.. code-block:: cfg

    [selenium-server]
    debug = true
    log = selenium-server.log

You can also specify the path to the configuration file with the ``--selenose-config`` option on the ``manage.py jenkins`` command line:

.. code:: bash

    $ python manage.py jenkins --help
    [...]
      selenose.tasks.selenium_server:
        --selenose-config=SELENOSE_CONFIGS
                            Load selenose configuration from config file(s). May
                            be specified multiple times; in that case, all config
                            files will be loaded and combined.

In your tests, just create a new ``Remote`` Web Driver calling the server and that's it:

.. code-block:: python

    from django.test import LiveServerTestCase

    from selenium import webdriver

    class TestCase(LiveServerTestCase):

        @classmethod
        def setUpClass(cls):
            cls.driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
            super(BaseTestCase, cls).setUpClass()

        @classmethod
        def tearDownClass(cls):
            super(BaseTestCase, cls).tearDownClass()
            cls.driver.quit()

        def test(self):
            driver.get(self.live_server_url)

.. _selenium-driver-task:

Selenium Driver Task
^^^^^^^^^^^^^^^^^^^^

This task provides a Selenium Web Driver to Selenium tests.

To enable it, edit your ``settings.py`` and append ``selenose.tasks.selenium_driver`` to ``JENKINS_TASKS``:

.. code:: python
    
    JENKINS_TASKS = [
        # Other tasks...
        'selenose.tasks.selenium_server',
    ]

If this setting does not exist yet, do not forget to create it with the default tasks:

.. code:: python
    
    JENKINS_TASKS = [
        'django_jenkins.tasks.run_pylint',
        'django_jenkins.tasks.with_coverage',
        'django_jenkins.tasks.django_tests',
        'selenose.tasks.selenium_driver',
    ]

But enabling this task is not enough, a :ref:`web-driver-environment` is also required.

The :ref:`web-driver-environment` are defined in a ``setup.cfg`` located in the current working directory, for instance:

.. code-block:: cfg

    [selenium-driver:sample]
    webdriver = firefox

You can also specify the path to the configuration file containing the environments with the ``--selenose-config`` option on the ``manage.py jenkins`` command line:

.. code:: bash

    $ python manage.py jenkins --help
    [...]
      selenose.tasks.selenium_driver:
        --selenose-config=SELENOSE_CONFIGS
                            Load selenose configuration from config file(s). May
                            be specified multiple times; in that case, all config
                            files will be loaded and combined.
        --selenium-driver=SELENIUM_DRIVER
                            Enable the provided environment.

To enable an environment, use the ``--selenium-driver`` option on the ``manage.py jenkins`` command line:

.. code:: bash

    $ python manage.py jenkins --selenium-driver=sample

Then the Web Driver is directly available in you tests with ``self.driver`` and there is no need to cleanup after use, selenose will do it for you:

.. code-block:: python

    from selenose.cases import LiveServerTestCase
    
    class TestCase(LiveServerTestCase):
        
        def test(self):
            self.driver.get(self.live_server_url)
            # Your test here...

Combining Server & Driver
^^^^^^^^^^^^^^^^^^^^^^^^^

To combine a Selenium Server and a Selenium Driver task, just enable them both in the settings: the ``command_executor`` option of the ``remote`` Web Driver will know the correct value to reach the Selenium Server.

.. code:: python
    
    JENKINS_TASKS = [
        # Other tasks...
        'selenose.tasks.selenium_server',
        'selenose.tasks.selenium_driver',
    ]


Tips
----

When writing tests, it's convenient to start a Selenium Server manually to reduce setup time when running tests. To do so, execute:

.. code-block:: bash

    $ selenium-server
    Starting... done!

    Quit the server with CONTROL-C.

Then type ``CONTROL-C`` or ``CTRL-BREAK`` to stop the server.

In this case, run your tests neither with the :ref:`selenium-server-plugin` not with the :ref:`selenium-server-task`.

