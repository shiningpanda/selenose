#-*- coding: utf-8 -*-
import unittest
import ConfigParser

import helpers

from selenium.webdriver import DesiredCapabilities

from selenose.configs import *

class ConfigsTestCase(unittest.TestCase):

    def test_filternone(self):
        self.assertEquals(dict(a=0, c=''), filternone(a=0, b=None, c=''))

    def test_server_config_custom_port(self):
        c = helpers.get_server_config(port=1234)
        self.assertEquals(1234, c.get_port())
        self.assertEquals('http://127.0.0.1:1234/wd/hub', c.get_command_executor())
        
    def test_server_config_default_port(self):
        c = helpers.get_server_config()
        self.assertEquals(4444, c.get_port())
        self.assertEquals('http://127.0.0.1:4444/wd/hub', c.get_command_executor())

    def test_section(self):
        # Create and fill a parser
        parser = ConfigParser.RawConfigParser()
        parser.add_section('toto')
        parser.set('toto', 'tata', '1')
        parser.set('toto', 'tutu', 'true')
        parser.set('toto', 'yop', 'abc')
        # Create a section from it
        section = Section(parser, 'toto')
        # Checks
        self.assertTrue(section.has('tata'))
        self.assertFalse(section.has('foobar'))
        self.assertEquals('abc', section.get('yop'))
        self.assertEquals(1, section.getint('tata'))
        self.assertTrue(section.getboolean('tutu'))
        self.assertEquals(set(['yop', 'tata', 'tutu']), set(section.options()))

    def test_chrome_env_default(self):
        env = helpers.get_chrome_env()
        self.assertEquals(None, env.get_port())
        self.assertEquals(None, env.get_executable_path())
        self.assertEquals(None, env.get_desired_capabilities())

    def test_chrome_env_custom(self):
        env = helpers.get_chrome_env(options=dict(
            port=1234,
            executable_path='/toto/chromedriver',
            desired_capabilities='firefox',    # Don't do this ;-)        
        ))
        self.assertEquals(1234, env.get_port())
        self.assertEquals('/toto/chromedriver', env.get_executable_path())
        self.assertEquals(DesiredCapabilities.FIREFOX, env.get_desired_capabilities())

    def test_firefox_env_default(self):
        env = helpers.get_firefox_env()
        self.assertEquals(None, env.get_timeout())

    def test_firefox_env_custom(self):
        env = helpers.get_firefox_env(options=dict(
            timeout=10,
        ))
        self.assertEquals(10, env.get_timeout())

    def test_ie_env_default(self):
        env = helpers.get_ie_env()
        self.assertEquals(None, env.get_port())
        self.assertEquals(None, env.get_timeout())

    def test_ie_env_custom(self):
        env = helpers.get_ie_env(options=dict(
            port=1234,
            timeout=10,
        ))
        self.assertEquals(1234, env.get_port())
        self.assertEquals(10, env.get_timeout())

    def test_remote_env_default_server_default(self):
        env = helpers.get_remote_env()
        self.assertEquals('http://127.0.0.1:4444/wd/hub', env.get_command_executor())
        self.assertEquals(None, env.get_desired_capabilities())

    def test_remote_env_default_server_custom(self):
        env = helpers.get_remote_env(
            server_options=dict(
                port=1234,
            )
        )
        self.assertEquals('http://127.0.0.1:1234/wd/hub', env.get_command_executor())
        self.assertEquals(None, env.get_desired_capabilities())

    def test_remote_env_custom_server_custom(self):
        env = helpers.get_remote_env(
            options=dict(
                command_executor='http://127.0.0.1:1234/wd/hub',
                desired_capabilities='opera',
            ),
            server_options=dict(
                port=5678,
            )
        )
        self.assertEquals('http://127.0.0.1:1234/wd/hub', env.get_command_executor())
        self.assertEquals(DesiredCapabilities.OPERA, env.get_desired_capabilities())

    def test_parse_desired_capabilities(self):
        env = helpers.get_remote_env(
            options=dict(
                desired_capabilities='browserName=firefox,platform=ANY',
            ),
        )
        self.assertEquals(dict(browserName='firefox', platform='ANY'), env.get_desired_capabilities())     

    def test_driver_config_builtins_chrome(self):
        c = helpers.get_driver_config({})
        env = c.getenv('chrome')
        self.assertTrue(isinstance(env, ChromeEnv))

    def test_driver_config_builtins_firefox(self):
        c = helpers.get_driver_config({})
        env = c.getenv('firefox')
        self.assertTrue(isinstance(env, FirefoxEnv))
        
    def test_driver_config_builtins_ie(self):
        c = helpers.get_driver_config({})
        env = c.getenv('ie')
        self.assertTrue(isinstance(env, IeEnv))

    def test_driver_config_builtins_remote(self):
        c = helpers.get_driver_config({})
        env = c.getenv('remote-htmlunit')
        self.assertTrue(isinstance(env, RemoteEnv))
        self.assertEquals(DesiredCapabilities.HTMLUNIT, env.get_desired_capabilities())

if __name__ == '__main__':
    unittest.main()