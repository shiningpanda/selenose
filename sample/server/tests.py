#-*- coding: utf-8 -*-
import nose
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class TestCase(unittest.TestCase):
    
    def test(self):
        # Get a driver
        driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
        # Be able to quit in any cases
        try:
            # Open Google search page
            driver.get('http://www.google.com')
            # Get the query field and input the text to search followed by enter
            driver.find_element_by_name('q').send_keys('ShiningPanda', Keys.RETURN)
            # Catch timeouts to display a nice message
            try:
                # Wait till found search query in title
                WebDriverWait(self.driver, 5).until(lambda driver : driver.title.lower().startswith('shiningpanda'))
            # Not found, this test failed
            except TimeoutException: self.fail('Google search failed')
        # Quit after test
        finally: driver.quit()
         
if __name__ == '__main__':
    nose.main()
