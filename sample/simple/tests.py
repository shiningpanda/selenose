#-*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

class TestCase(unittest.TestCase):
    
    def test(self):
        '''
        Searches for the term `Cheese` on Google and then check the result page’s title.
        '''
        driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
        driver.get('http://www.google.com')
        driver.find_element_by_name('q').send_keys('Cheese!')
        driver.find_element_by_name('btnK').click()
        try:
            WebDriverWait(driver, 10).until(lambda driver : driver.title.lower().startswith('cheese! -'))
        except TimeoutException:
            driver.quit()
            self.fail('failed to find page title')
        else:
            driver.quit()
         
if __name__ == '__main__':
    unittest.main()
