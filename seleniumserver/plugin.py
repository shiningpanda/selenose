#-*- coding: utf-8 -*-
from nose import plugins

from seleniumserver import server

class Plugin(plugins.Plugin):
    '''
    Nose plugin.
    '''

    name = 'selenium-server'

    def help(self): return 'Start a Selenium server before running tests.'

    def configure(self, options, conf):
        '''
        Configure the plugin.
        '''
        # Call super
        super(Plugin, self).configure(options, conf)
        # Initialize the server
        self.server = server.SeleniumServer(server.load_options(getattr(conf, 'files', [])))

    def begin(self):
        '''
        Start the Selenium server.
        '''
        self.server.start()
    
    def finalize(self, result):
        '''
        Stop the Selenium server.
        '''
        self.server.stop()
