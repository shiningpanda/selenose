#-*- coding: utf-8 -*-
from djangosanetesting.cases import HttpTestCase

from selenose.cases import SeleniumTestCase

class PollsTestCase(SeleniumTestCase, HttpTestCase):
    
    def test_vote(self):
        # Open the polls page
        self.driver.get('http://localhost:8000/polls/')
        # Get the link to the poll "How is selenose?"
        poll = self.driver.find_element_by_link_text('How is selenose?')
        # Click on the link
        poll.click()
        # Get the available choices
        choices = self.driver.find_elements_by_name('choice')
        # Check that only two choices: "Cool" and "Super cool"
        self.assertEquals(2, len(choices))
        # Select "Super cool"
        choices[1].click()
        # Submit the form
        choices[1].submit()
        # Get the poll results
        lis = self.driver.find_elements_by_tag_name('li')
        # Check that results are displayed for each choices (two choices)
        self.assertEquals(2, len(lis))
        # Check that "Cool" has no votes
        self.assertEquals('Cool? -- 0 votes', lis[0].text)
        # Check that our vote for "Super cool" was well stored
        self.assertEquals('Super cool? -- 1 vote', lis[1].text)

