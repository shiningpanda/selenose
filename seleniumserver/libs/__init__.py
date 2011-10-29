#-*- coding: utf-8 -*-
import os
import glob
import urllib2

from seleniumserver import consts

def selenium_server_bn():
    '''
    Get the Selenium server jar name.
    '''
    return 'selenium-server-standalone-%s.jar' % consts.SELENIUM_SERVER_VERSION

def selenium_server_url():
    '''
    Get the Selenium server jar url.
    '''
    return 'http://selenium.googlecode.com/files/%s' % selenium_server_bn()

def selenium_server_path():
    '''
    Get the Selenium server jar path.
    '''
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), selenium_server_bn())

def clean(all=False):
    '''
    Delete jars in this folder. If provided flag set to true, also delete current jar.
    '''
    folder = os.path.dirname(selenium_server_path())
    for fp in glob.glob(os.path.join(folder, '*.jar')):
        if all or os.path.basename(fp) != selenium_server_bn():
            os.remove(os.path.join(folder, fp))

def download(force=False):
    '''
    Download Selenium server jar.
    '''
    fp = selenium_server_path()
    exists = os.path.exists(fp)
    if not exists or force:
        if os.path.exists(fp):
            os.remove(fp)
        url = selenium_server_url()
        fd = open(selenium_server_path(), 'wb')
        try:
            fd.write(urllib2.urlopen(url).read())
        except Exception, e:
            fd.close()
            os.remove(fp)
            raise e
        fd.close()
