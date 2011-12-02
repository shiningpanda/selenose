#-*- coding: utf-8 -*-
import unittest

from selenium import webdriver

from selenose import libs

from helpers import get_server

class ServerTestCase(unittest.TestCase):
    
    def test_build_cmd_line_1(self):
        self.assertEquals(['java', '-jar', libs.selenium_server_path(), ], get_server().build_cmd_line())

    def test_build_cmd_line_2(self):
        self.assertEquals(['-debug'], get_server(debug='true').build_cmd_line()[3:])

    def test_build_cmd_line_3(self):
        self.assertEquals([], get_server(debug='false').build_cmd_line()[3:])

    def test_build_cmd_line_4(self):
        self.assertEquals(['-log', 'selenium-server.log', ], get_server(log='selenium-server.log').build_cmd_line()[3:])

    def test_build_cmd_line_5(self):
        self.assertEquals(['-userContentTransformation', 'a', 'b'], get_server(userContentTransformation='a b').build_cmd_line()[3:])

    def test_start_stop(self):
        s = get_server(log='selenium-server.log')
        try:
            s.start()
            driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
            driver.get('http://www.google.com/')
            driver.quit()
        finally:
            s.stop()

if __name__ == '__main__':
    unittest.main()
