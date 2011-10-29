#-*- coding: utf-8 -*-
import unittest

from selenium import webdriver

from nose.plugins import PluginTester

from seleniumserver.plugin import Plugin

class PluginTestCase(PluginTester, unittest.TestCase):
    
    activate = '--with-selenium-server'
    
    plugins = [ Plugin(), ]

    def test(self):
        assert 'OK' in self.output
    def makeSuite(self):
        class TC(unittest.TestCase):
            def runTest(self):
                driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
                driver.get('http://www.google.com/')
                driver.quit()
        return unittest.TestSuite([TC()])
    
if __name__ == '__main__':
    unittest.main()