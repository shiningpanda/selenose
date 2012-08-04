# -*- coding: utf-8 -*-
from django_jenkins.tasks import BaseTask

from selenose.server import Server
from selenose.configs import ServerConfig
from selenose.tasks import all_config_files

class Task(BaseTask):
    '''
    Start a SELENIUM server before the tests.
    '''

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
