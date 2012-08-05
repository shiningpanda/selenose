#-*- coding: utf-8 -*-
from optparse import make_option

from nose import config

def all_config_files(options):
    '''
    Get the list of configuration files.
    '''
    # Get default configuration files
    files = config.all_config_files()
    # Get files from options
    files.extend(getattr(options, 'selenose_configs', []))
    # Return the full list
    return files

def make_config_option():
    '''
    Make the option for the configuration files.
    '''
    # Delegate
    return make_option(
        '--selenose-config',
        action='append',
        default=[],
        dest='selenose_configs',
        help='Load selenose configuration from config file(s). May be specified multiple times; in that case, all config files will be loaded and combined.',
    )