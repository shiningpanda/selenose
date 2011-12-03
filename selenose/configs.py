#-*- coding: utf-8 -*-
import os
import uuid
import tempfile

try: 
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

from selenium.webdriver import DesiredCapabilities, Chrome, Firefox, Ie, Remote

def filternone(**kwargs):
    '''
    If a value is not defined, pop it.
    '''
    # Get the copy of the dictionary
    copy = dict(kwargs)
    # For each item, check that a value is provided
    for key, value in kwargs.items():
        # Check that value is provided
        if value is None:
            # If not provided, pop it
            copy.pop(key)
    # Return the cleaned dictionary
    return copy

class Section(object):
    '''
    A configuration section.
    '''
    
    def __init__(self, parser, section):
        '''
        Initialize the section with a parser and the name of the section.
        '''
        # Store the parser
        self.parser = parser
        # Store the name of the section
        self.section = section

    def options(self):
        '''
        List of available options in this section.
        '''
        # Delegate
        return self.parser.options(self.section)

    def has(self, option):
        '''
        Check if this section has the provided option.
        '''
        # Delegate
        return self.parser.has_option(self.section, option)

    def get(self, option):
        '''
        Get the value for the provided option.
        '''
        # Delegate
        return self.parser.get(self.section, option)

    def getint(self, option):
        '''
        Get the value as integer for the provided option.
        '''
        # Delegate
        return self.parser.getint(self.section, option)

    def getfloat(self, option):
        '''
        Get the value as float for the provided option.
        '''
        # Delegate
        return self.parser.getfloat(self.section, option)

    def getboolean(self, option):
        '''
        Get the value as boolean for the provided option.
        '''
        # Delegate
        return self.parser.getboolean(self.section, option)

class ServerConfig(Section):
    '''
    SELENIUM server configuration.
    '''
    # Store cardinality of each option
    cardinalities = dict(
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
    
    def __init__(self, files):
        '''
        Initialize the configuration with a list of files.
        '''
        # Section
        section = 'selenium-server'
        # Create a new parser
        parser = RawConfigParser()
        # Create the section anyway
        parser.add_section(section)
        # Read the provided files
        parser.read(files)
        # Initialize the server section
        super(ServerConfig, self).__init__(parser, section)
        # Check if must provided a temporary log file
        self.is_log_temp = not self.has('log')
        # Create a temporary log file
        if self.is_log_temp:
            # Create and set the log file
            self.parser.set(section, 'log', os.path.join(tempfile.gettempdir(), 'selenose_%s.log' % uuid.uuid4().hex))

    def get_log(self):
        '''
        Get the log folder.
        '''
        return self.get('log')
    
    def get_port(self):
        '''
        Get the port.
        '''
        # Check if defined
        if self.has('port'):
            # If defined, get it as an integer
            return self.getint('port')
        # Else use default value
        return 4444
    
    def get_command_executor(self):
        '''
        Get the command executor.
        '''
        return 'http://127.0.0.1:%d/wd/hub' % self.get_port()

class BaseEnv(Section):
    '''
    Base class for the SELENIUM environment.
    '''

    def __init__(self, name, parser, section, *args, **kwargs):
        '''
        Initialize the environment.
        '''
        # Call super
        super(BaseEnv, self).__init__(parser, section)
        # Store the name of the environment
        self.name = name

    @property
    def key(self):
        '''
        Key for this environment, must be defined by subclasses.
        '''
        raise NotImplementedError

    def get_port(self):
        '''
        Get the port.
        '''
        # Check if defined
        if self.has('port'):
            # If defined return the integer value, else return nothing
            return self.getint('port')

    def get_timeout(self):
        '''
        Get the timeout.
        '''
        # Check if defined
        if self.has('timeout'):
            # If defined return the integer value, else return nothing
            return self.getint('timeout')

    def get_desired_capabilities(self):
        '''
        Get the desired capabilities.
        '''
        # Check if defined in configuration
        if self.has('desired_capabilities'):
            # If defined, get its value
            capabilities = self.get('desired_capabilities')
            # Check if a standard capability
            if hasattr(DesiredCapabilities, capabilities.upper()):
                # If standard one, return its value
                return getattr(DesiredCapabilities, capabilities.upper())
            # Else parse the value to return a map
            asmap = {}
            # Split on separator
            for capability in capabilities.split(','):
                # Get the key and value
                key, value = capability.split('=', 1)
                # Store them stripped
                asmap[key.strip()] = value.strip()
            # Return the map
            return asmap

    def create(self):
        '''
        Create a driver from this environment, this should be defined by subclasses.
        '''
        raise NotImplementedError

class ChromeEnv(BaseEnv):
    '''
    CHROME environment.
    '''
    # Key for this environment
    key = 'chrome'

    def get_executable_path(self):
        '''
        Get the path to the executable.
        '''
        # Check if defined
        if self.has('executable_path'):
            # If defined, return its value, else return nothing
            return self.get('executable_path')

    def create(self):
        '''
        Create a new driver.
        '''
        return Chrome(**filternone(
            executable_path=self.get_executable_path(),
            port=self.get_port(),
            desired_capabilities=self.get_desired_capabilities(),
        ))

class FirefoxEnv(BaseEnv):
    '''
    FIREFOX environment.
    '''
    # Key for this environment
    key = 'firefox'

    def create(self):
        '''
        Create a new driver.
        '''
        return Firefox(**filternone(
            timeout=self.get_timeout(),
        ))

class IeEnv(BaseEnv):
    '''
    Internet explorer environment.
    '''
    # Key for this environment
    key = 'ie'
        
    def create(self):
        '''
        Create a new driver.
        '''
        return Ie(**filternone(
            port=self.get_port(),
            timeout=self.get_timeout(),
        ))

class RemoteEnv(BaseEnv):
    '''
    Remote driver environment.
    '''
    # Key for this environment
    key = 'remote'
    
    def __init__(self, name, parser, section, server):
        '''
        Initialize the environment with an additional server configuration to be able to get its port.
        '''
        # Call super
        super(RemoteEnv, self).__init__(name, parser, section)
        # Store the server configuration
        self.server = server
    
    def get_command_executor(self):
        '''
        Get the command executor.
        '''
        # CHeck if defined
        if self.has('command_executor'):
            # If defined, return it
            return self.get('command_executor')
        # Else return the server one
        return self.server.get_command_executor()
    
    def create(self):
        '''
        Create a new driver.
        '''
        return Remote(**filternone(
            command_executor=self.get_command_executor(),
            desired_capabilities=self.get_desired_capabilities(),
        ))

class DriverConfig(object):
    '''
    SELENIUM driver configuration.
    '''
    # Available environments
    envs = {
        ChromeEnv.key : ChromeEnv,
        FirefoxEnv.key: FirefoxEnv,
        IeEnv.key     : IeEnv,
        RemoteEnv.key : RemoteEnv,
    }
    
    def __init__(self, files):
        '''
        Initialize the configuration with a list of files.
        '''
        # Create a new parser
        self.parser = RawConfigParser()
        # Load default configuration
        self.builtins()
        # Load the files
        self.parser.read(files)
        # Store a server configuration
        self.server = ServerConfig(files)
    
    def builtins(self):
        '''
        Load default configurations.
        '''
        # For simple environment, only add a section with its driver value
        for env in (ChromeEnv, FirefoxEnv, IeEnv):
            # Get the name of the section
            section = self.get_section(env.key)
            # Add the section
            self.parser.add_section(section)
            # Add the driver value
            self.parser.set(section, 'webdriver', env.key)
        # For the remote driver, create an entry for each capabilities
        for capabilities in [ c.lower() for c in dir(DesiredCapabilities) if c == c.upper() ] :
            # Get the name of the section
            section = self.get_section('remote-%s' % capabilities)
            # Add the section
            self.parser.add_section(section)
            # Set the driver value
            self.parser.set(section, 'webdriver', 'remote')
            # Set the capabilities
            self.parser.set(section, 'desired_capabilities', capabilities)
    
    def get_section(self, name):
        '''
        Get the name of the section given the name of the environment.
        '''
        return 'selenium-driver:%s' % name
    
    def getenv(self, name):
        '''
        Get the environment from its name.
        '''
        # Get the name of the section
        section = self.get_section(name)
        # Get the option that lets us distinguish the right environment class
        option = 'webdriver'
        # Get the driver value
        driver = self.parser.get(section, option)
        # Deduce the environment class
        env = self.envs.get(driver)
        # If not found, this is an unexpected value
        if not env:
            # This is an error
            raise ValueError('invalid value for %s.%s: %s' % (section, option, driver))
        # Create a new instance for the environment
        return env(name, self.parser, section, self.server)

    
                