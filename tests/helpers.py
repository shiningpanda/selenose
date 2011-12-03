#-*- coding: utf-8 -*-
import os
try: 
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

from selenose.configs import *
from selenose.server import Server

def create_section_file(dico):
    '''
    Convert a dictionary of dictionary in section file.
    '''
    parser = RawConfigParser()
    for section, options in dico.items():
        parser.add_section(section)
        for option, value in options.items():
            parser.set(section, option, value)
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'selenose.cfg')
    fd = open(fp, 'w')
    parser.write(fd)
    fd.close()
    return fp

def get_server_config(**kwargs):
    '''
    Get a server configuration.
    '''
    return ServerConfig([ create_section_file({'selenium-server': kwargs, }) ])

def get_server(**kwargs):
    '''
    Get a server.
    '''
    return Server(get_server_config(**kwargs))

def get_base_env(cls, name, section, options=None, server=None):
    '''
    Get a base environment.
    '''
    options = options or {}
    parser = RawConfigParser()
    parser.add_section(section)
    for option, value in options.items():
        parser.set(section, option, value)
    return cls(name, parser, section, server)

def get_chrome_env(name='chrome', section='selenium-driver:chrome', options=None):
    '''
    Get a CHROME environment.
    '''
    return get_base_env(ChromeEnv, name, section, options)

def get_firefox_env(name='firefox', section='selenium-driver:firefox', options=None):
    '''
    Get a FIREFOX environment.
    '''
    return get_base_env(FirefoxEnv, name, section, options)

def get_ie_env(name='ie', section='selenium-driver:ie', options=None):
    '''
    Get an IE environment.
    '''
    return get_base_env(IeEnv, name, section, options)

def get_remote_env(name='remote', section='selenium-driver:remote', options=None, server_options=None):
    '''
    Get a remote environment.
    '''
    return get_base_env(RemoteEnv, name, section, options, get_server_config(**(server_options or {})))

def get_driver_config(dico):
    '''
    Get a driver configuration from a dictionary.
    '''
    return DriverConfig([ create_section_file(dico), ])
