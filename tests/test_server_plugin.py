#-*- coding: utf-8 -*-
import unittest

from selenium import webdriver

from nose.plugins import PluginTester

from selenose.plugins import SeleniumServerPlugin

class PluginTestCase(PluginTester, unittest.TestCase):
    
    activate = '--with-selenium-server'
    
    plugins = [ SeleniumServerPlugin(), ]

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