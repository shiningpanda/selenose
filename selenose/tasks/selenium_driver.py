# -*- coding: utf-8 -*-
from optparse import make_option

from django_jenkins.tasks import BaseTask

from selenose.configs import DriverConfig
from selenose.tasks import all_config_files, make_config_option

# Store the SELENIUM environment configuration
env = None

class Task(BaseTask):
    '''
    Create a SELENIUM driver.
    '''
    option_list = [
        make_config_option(),
        make_option(
            '--selenium-driver',
            action='store',
            dest='selenium_driver',
            help='Enable the provided environment.'
        ),
    ]

    def __init__(self, test_labels, options):
        '''
        Store the environment configuration.
        '''
        # Call super
        super(Task, self).__init__(test_labels, options)
        # Get the environment
        selenium_driver = options.get('selenium_driver')
        # Check if an environment is provided
        if not selenium_driver:
            # Not provided, raise
            raise ValueError('please provide a driver environment with the --selenium-driver option')
        # Get the global environments variable containing the SELENIUM environment
        global env
        # Store the environment
        env = DriverConfig(all_config_files(options)).getenv(selenium_driver)
