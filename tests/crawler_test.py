from unittest import TestCase
from modules import crawler


class TestCrawler(TestCase):
    def test__data_check(self):
        link = "https://stackoverflow.com"
        wrong_link = link + 'omg'
        path = ''
        wrong_thread_amount = -4
        craw = crawler.Crawler(wrong_link, path, 3)
        with self.assertRaises(Exception):
            craw._data_check()
        craw = crawler.Crawler(link, path, wrong_thread_amount)
        with self.assertRaises(Exception):
            craw._data_check()

    # def test_robots(self,link):
    #     self.assertEqual(link + '/robots.txt',)
