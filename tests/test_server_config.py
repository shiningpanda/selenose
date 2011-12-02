#-*- coding: utf-8 -*-
import unittest
import ConfigParser

from helpers import get_server_config

class ServerConfigTestCase(unittest.TestCase):
    
    def test_custom_port(self):
        c = get_server_config(port=1234)
        self.assertEquals(1234, c.get_port())
        self.assertEquals('http://127.0.0.1:1234/wd/hub', c.get_command_executor())
        
    def test_default_port(self):
        c = get_server_config()
        self.assertEquals(4444, c.get_port())
        self.assertEquals('http://127.0.0.1:4444/wd/hub', c.get_command_executor())

if __name__ == '__main__':
    unittest.main()