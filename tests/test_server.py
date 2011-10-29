#-*- coding: utf-8 -*-
import unittest

from selenium import webdriver

from seleniumserver import server, libs

class ServerTestCase(unittest.TestCase):
    
    def test_build_cmd_line_1(self):
        self.assertEquals(['java', '-jar', libs.selenium_server_path(), ], server.build_cmd_line({}))

    def test_build_cmd_line_2(self):
        self.assertEquals(['-debug'], server.build_cmd_line(dict(debug='true'))[3:])

    def test_build_cmd_line_3(self):
        self.assertEquals([], server.build_cmd_line(dict(debug='false'))[3:])

    def test_build_cmd_line_4(self):
        self.assertEquals(['-log', 'selenium-server.log', ], server.build_cmd_line(dict(log='selenium-server.log'))[3:])

    def test_build_cmd_line_5(self):
        self.assertEquals(['-userContentTransformation', 'a', 'b'], server.build_cmd_line(dict(userContentTransformation='a b'))[3:])

    def test_start_stop(self):
        s = server.SeleniumServer(dict(log='selenium-server.log'))
        try:
            s.start()
            driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
            driver.get('http://www.google.com/')
            driver.quit()
        finally:
            s.stop()

if __name__ == '__main__':
    unittest.main()
