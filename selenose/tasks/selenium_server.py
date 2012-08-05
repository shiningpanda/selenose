# -*- coding: utf-8 -*-
from django.conf import settings

from django_jenkins.tasks import BaseTask

from selenose.server import Server
from selenose.configs import ServerConfig
from selenose.tasks import all_config_files, make_config_option

class Task(BaseTask):
    '''
    Start a SELENIUM server before the tests.
    '''

    # Add option for configuration file only if not set by the driver task.
    option_list = [] if 'selenose.tasks.selenium_driver' in getattr(settings, 'JENKINS_TASKS', []) else [ make_config_option() ]

    def __init__(self, test_labels, options):
        '''
        Store the server.
        '''
        # Call super
        super(Task, self).__init__(test_labels, options)
        # Create the server
        self.server = Server(ServerConfig(all_config_files(options)))
        
    def setup_test_environment(self, **kwargs):
        '''
        Start the SELENIUM server.
        '''
        self.server.start()
    
    def teardown_test_environment(self, **kwargs):
        '''
        Stop the SELENIUM server.
        '''
        self.server.stop()
