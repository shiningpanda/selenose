#-*- coding: utf-8 -*-
import os
import sys
import shlex
import signal
import pexpect
import ConfigParser

import nose.config

from seleniumserver import libs

# Available server options
server_options = dict(
    port                        = 1,
    timeout                     = 1,
    interactive                 = 0,
    singleWindow                = 0,
    profilesLocation            = 1,
    forcedBrowserMode           = 1,
    forcedBrowserModeRestOfLine = 1,
    userExtensions              = 1,
    browserSessionReuse         = 0,
    avoidProxy                  = 0,
    firefoxProfileTemplate      = 1,
    debug                       = 0,
    browserSideLog              = 0,
    ensureCleanSession          = 0,
    trustAllSSLCertificates     = 0,
    log                         = 1,
    htmlSuite                   = 4,
    proxyInjectionMode          = 0,
    dontInjectRegex             = 1,
    userJsInjection             = 1,
    userContentTransformation   = 2,
)

def build_cmd_line(options):
    '''
    Build the server options.
    '''
    # Get the begin of the command line
    line = ['java', '-jar', libs.selenium_server_path(), ]
    # Go threw the server options
    for option in options.keys():
        # Check if this option exists
        if server_options.has_key(option):
            # Get the number of arguments for this option
            n = server_options.get(option)
            # Get the value for this option
            val = options.get(option)
            # If no argument, this is a boolean option
            if n == 0:
                # Check if this option is enabled
                if str(val).upper() in ('1', 'T', 'TRUE', 'ON'):
                    # If enabled add to command line
                    line.append('-%s' % option)
            # Check if option with one argument
            elif n == 1:
                # Add it
                line.extend(('-%s' % option, val))
            # Option with multiple arguments
            else:
                # Add the option
                line.append('-%s' % option)
                # Parse the arguments and add them
                line.extend(shlex.split(val))
    # Return the command line
    return line

def load_options(files):
    '''
    Load the server options from the provided files.
    '''
    # Store options
    options = {}
    # Go threw the provided files
    for fp in files:
        # Get a configuration parser
        config = ConfigParser.RawConfigParser()
        # Read the configurations
        config.read(fp)
        # The section to look for
        section = 'selenium-server'
        # Check if this section exists
        if config.has_section(section):
            # Go threw the options
            for option in config.options(section):
                # Store in dictionary
                options[option] = config.get(section, option)
    # Return the options
    return options

class SeleniumServer(object):
    '''
    Start and stop Selenium server.
    '''
    
    def __init__(self, options):
        '''
        Initialize.
        '''
        # Options
        self.options = options
        # Store process pointer
        self.process = None

    def start(self):
        '''
        Start the server.
        '''
        # Check that not already started
        assert self.process is None
        # Get the command line
        line = build_cmd_line(self.options)
        # Spawn the process
        self.process = pexpect.spawn(line[0], args=line[1:])
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

def run():
    '''
    Start the server and wait for signal to stop it.
    '''
    # Create the server
    server = SeleniumServer(load_options(nose.config.all_config_files()))
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
