#-*- coding: utf-8 -*-
from selenose.cases import SeleniumTestCase

from djangosanetesting.cases import HttpTestCase

class AdminTestCase(SeleniumTestCase, HttpTestCase):
    
    def test_login(self):
        # Open the administration page
        self.driver.get('http://localhost:8000/admin/')
        # Enter the name of the user
        self.driver.find_element_by_id('id_username').send_keys('admin')
        # Get the password input
        password = self.driver.find_element_by_id('id_password')
        # Type password
        password.send_keys('admin')
        # Submit the form
        password.submit()
        # Check that welcomed
        self.assertTrue(self.driver.find_element_by_id('user-tools').text.startswith('Welcome'))

