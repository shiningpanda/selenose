#-*- coding: utf-8 -*-
import os
import sys
import glob

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

def selenium_server_bn(version):
    '''
    Get the SELENIUM server jar name.
    '''
    return 'selenium-server-standalone-%s.jar' % version

def selenium_server_url(version):
    '''
    Get the SELENIUM server jar URL.
    '''
    return 'http://selenium.googlecode.com/files/%s' % selenium_server_bn(version)

def selenium_server_path(version=None):
    '''
    Get the SELENIUM server jar path.
    '''
    # Check if version is specified
    if version is None:
        # Get the version
        from selenose.__version__ import __version__
        # Copy the version
        version = __version__
    # Get the path
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), selenium_server_bn(version))

def clean(version, full=False):
    '''
    Delete jars in this folder. If provided flag set to true, also delete current jar.
    '''
    # Get the folder containing the jars
    folder = os.path.dirname(selenium_server_path(version))
    # Look for jars
    for fp in glob.glob(os.path.join(folder, '*.jar')):
        # Delete all jars, including current one if full clean required
        if full or os.path.basename(fp) != selenium_server_bn(version):
            # Delete file
            os.remove(os.path.join(folder, fp))

def download(version, force=False):
    '''
    Download SELENIUM server jar.
    '''
    # Get the jar path
    fp = selenium_server_path(version)
    # Check if already exists
    exists = os.path.exists(fp)
    # If jar does not exist or if download is forced, download it
    if not exists or force:
        # If file exist, delete it
        if os.path.exists(fp):
            # Delete the file
            os.remove(fp)
        # Get the URL
        url = selenium_server_url(version)
        # Log
        print('downloading %s from %s' % (os.path.basename(fp), url))
        # Get the target file descriptor
        fd = open(fp, 'wb')
        # Be able to delete the file if something does wrong
        try:
            # Download the file
            fd.write(urlopen(url).read())
        # Something goes wrong, cleanup
        except Exception as e:
            # Close the file descriptor
            fd.close()
            # Delete the partial file
            os.remove(fp)
            # Raise
            raise e
        # Close the file descriptor if download is successful
        fd.close()

