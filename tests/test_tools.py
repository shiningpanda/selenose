#-*- coding: utf-8 -*-
import unittest

from seleniumserver.configs import filternone

class ToolsTestCase(unittest.TestCase):
    
    def test_filternone(self):
        self.assertEquals(dict(a=0, c=''), filternone(a=0, b=None, c=''))
    
if __name__ == '__main__':
    unittest.main()