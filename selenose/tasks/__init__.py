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
