#-*- coding: utf-8 -*-
import nose

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from selenose.cases import SeleniumTestCase

class TestCase(SeleniumTestCase):
    
    def test(self):
        # Open Google search page
        self.driver.get('http://www.google.com')
        # Get the query field and input the text to search followed by enter
        self.driver.find_element_by_name('q').send_keys('ShiningPanda', Keys.RETURN)
        # Catch timeouts to display a nice message
        try:
            # Wait till found search query in title
            WebDriverWait(self.driver, 5).until(lambda driver : driver.title.lower().startswith('shiningpanda'))
        # Not found, this test failed
        except TimeoutException: self.fail('Google search failed')

if __name__ == '__main__':
    nose.main()