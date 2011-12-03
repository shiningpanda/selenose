#-*- coding: utf-8 -*-
import os
import sys
import time
import uuid
import shlex
import optparse
import tempfile
import subprocess

try: input = raw_input
except: pass

import nose.config

from selenose import libs
from selenose.configs import ServerConfig

def expect(fd, pattern, timeout):
    '''
    Look for a string in a log file.
    '''
    # Initialize the log content
    body = ''
    # Get the deadline
    deadline = time.time() + timeout
    # Look for the string while deadline in not reached
    while time.time() < deadline:
        # Flush
        fd.flush()
        # Open the log file
        log = open(fd.name)
        # Read the end of the file
        body = log.read()
        # Close the file
        log.close()
        # Check if sting is in the read content
        if pattern in body:
            # If inside, we're successful
            return True, body
        # Else wait a little bit
        time.sleep(1)
    # Not found
    return False, body

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
        # Store log file descriptor
        self.log = None

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
        # Store 
        self.log = open(os.path.join(tempfile.gettempdir(), 'selenose_%s.log' % uuid.uuid4().hex), 'w')
        # Spawn the process
        self.process = subprocess.Popen(self.build_cmd_line(), stdout=self.log, stderr=subprocess.STDOUT)
        # Check when the server is started (wait at most 60 seconds)
        success, message = expect(self.log, 'Started org.openqa.jetty.jetty.Server', timeout=60)
        # Check if started
        if not success:
            # Stop it
            self.stop()
            # And re raise the exception
            raise AssertionError('failed to start server:\n%s' % message)
    
    def stop(self):
        '''
        Stop the server.
        '''
        # Check if process started
        if self.process:
            # Stop the server
            self.process.terminate()
            # Reset process
            self.process = None
            # Get the log file path
            fp = self.log.name
            # Close file descriptor
            self.log.close()
            # Reset the log file descriptor
            self.log = None
            # Check if clean the log
            if os.path.isfile(fp):
                # Delete the log file
                os.remove(fp)

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
        input()
    # Stop server
    except KeyboardInterrupt: server.stop()
