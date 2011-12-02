#-*- coding: utf-8 -*-
import unittest
import ConfigParser

from seleniumserver.configs import Section

class SectionTestCase(unittest.TestCase):
    
    def test(self):
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

if __name__ == '__main__':
    unittest.main()