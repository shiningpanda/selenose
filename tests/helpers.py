#-*- coding: utf-8 -*-
import os
import ConfigParser

from seleniumserver.server import Server
from seleniumserver.configs import ServerConfig, DriverConfig

def create_section_file(dico):
    '''
    Convert a dictionary of dictionary in section file.
    '''
    parser = ConfigParser.RawConfigParser()
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

def get_base_env(cls, name, **kwargs):
    return cls(name, [ create_section_file({'selenium-server': kwargs, }), ])


def get_driver_config(**kwargs):
    '''
    Get a server configuration.
    '''
    return DriverConfig([ create_section_file(kwargs), ])
