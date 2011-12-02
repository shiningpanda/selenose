#-*- coding: utf-8 -*-
import os
import sys
import shlex
import signal
import pexpect
import optparse

import nose.config

from seleniumserver import libs
from seleniumserver.configs import ServerConfig

class Server(object):
    '''
    Start and stop SELENIUM server.
    '''
    
    def __init__(self, config):
        '''
        Initialize.
        '''
        # Configuration
        self.config = config
        # Store process pointer
        self.process = None

    def build_cmd_line(self):
        '''
        Build the server options.
        '''
        # Get the begin of the command line
        line = ['java', '-jar', libs.selenium_server_path(), ]
        # Go threw the server options
        for option in self.config.cardinalities.keys():
            # Check if this option exists
            if self.config.has(option):
                # Get the number of arguments for this option
                cardinality = self.config.cardinalities.get(option)
                # If no argument, this is a boolean option
                if cardinality == 0:
                    # Check if this option is enabled
                    if self.config.getboolean(option):
                        # If enabled add to command line
                        line.append('-%s' % option)
                # Check if option with one argument
                elif cardinality == 1:
                    # Add it
                    line.extend(('-%s' % option, self.config.get(option)))
                # Option with multiple arguments
                else:
                    # Add the option
                    line.append('-%s' % option)
                    # Parse the arguments and add them
                    line.extend(shlex.split(self.config.get(option)))
        # Return the command line
        return line

    def start(self):
        '''
        Start the server.
        '''
        # Check that not already started
        assert self.process is None
        # Get the command line
        line = self.build_cmd_line()
        # Spawn the process
        self.process = pexpect.spawn(command=line[0], args=line[1:])
        # Be able to stop the server if pattern not found
        try:
            # Check when the server is started (wait at most 60 seconds)
            self.process.expect('Started org.openqa.jetty.jetty.Server', timeout=60)
        # Server failed to start
        except pexpect.TIMEOUT, e:
            # Stop it
            self.stop()
            # And re raise the exception
            raise e
    
    def stop(self):
        '''
        Stop the server.
        '''
        # Check if process started
        if self.process:
            # Send stop signal
            os.kill(self.process.pid, signal.SIGTERM)
            # Wait for the end of the process
            os.waitpid(self.process.pid, 0)
            # Reset
            self.process = None

def _run():
    '''
    Delegate with arguments coming from command line.
    '''
    # Delegate
    run(sys.argv)

def run(argv):
    '''
    Start the server and wait for signal to stop it.
    '''
    # Create a parser
    parser = optparse.OptionParser()
    # Configuration files
    parser.add_option('-c', '--config', dest='files', action='append', default=[], help='Load configuration from file. May be specified multiple times.', metavar='FILE')
    # Parser options
    options = parser.parse_args(argv)[0]
    # Get all the configuration files
    files = nose.config.all_config_files()
    # Add the ones coming from command line
    files.extend(options.files)
    # Create the server
    server = Server(ServerConfig(files))
    # Catch signals
    try:
        # Notify user
        sys.stdout.write('Starting... ')
        # Flush
        sys.stdout.flush()
        # Start server
        server.start()
        # Notify user
        sys.stdout.write('done!\n\n')
        # Get the command to exit the server
        quit_command = (sys.platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C'
        # Notify user
        sys.stdout.write('Quit the server with %s.\n' % quit_command)
        # Wait
        raw_input()
    # Stop server
    except KeyboardInterrupt: server.stop()
