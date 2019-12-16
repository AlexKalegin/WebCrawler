from unittest import TestCase
from modules import parser
from collections import deque


class TestPageParser(TestCase):
    def setUp(self):
        self.link = 'https://stackoverflow.com'
        self.saved_links = deque
        self.links = deque
        self.all_links = deque
        self.robots = self.link + '/robots.txt'
        self.page_parser = parser.Parser(self.link, self.all_links,
                                         self.saved_links, self.links, self.robots)

    def test__correct_link(self):
        self.assertEqual(self.page_parser.make_link_correct(self.link), self.link)
        self.assertEqual(self.page_parser.make_link_correct('questions'),
                         'https://stackoverflow.com/questions')
        self.assertEqual(self.page_parser.make_link_correct('/'),
                         'https://stackoverflow.com/')

    def test_save_links(self):
        self.assertEqual(self.page_parser.saved_links, self.saved_links)
