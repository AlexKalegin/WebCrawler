from collections import deque
from modules.parser import Parser
from modules import downloader
import urllib.request
from urllib.error import URLError
import os
import urllib.robotparser
import logging

module_log = logging.getLogger('WebCrawler.crawler')


class Crawler:
    """Главный класс краулера"""
    def __init__(self, link, path, thread_amount):
        self.link = link
        self.path = path
        self.all_links = [link]
        self.saved_links = deque()
        self.links = deque()
        self.robots = urllib.robotparser.RobotFileParser()
        self.thread_amount = thread_amount
        self.threads = []

    def start(self):
        """Метод для инициализации переменных"""
        self._data_check()
        self.robots.set_url(self.link + '/robots.txt')
        self.robots.read()
        self.links.append(self.link)
        self.saved_links.append(self.link)
        self._create_threads()
        self._start_threads()
        self._action()

    def _action(self):
        """Парсит ссылку из очереди"""
        while len(self.links) != 0:
            link = self.links.popleft()
            page = Parser(link, self.all_links, self.saved_links, self.links, self.robots)
            page.save_links()

    def _data_check(self):
        """Проверяет корректность введенных данных"""
        log = logging.getLogger('WebCrawler.crawler._data_check')
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except OSError:
                log.info('Path does not exist')
                raise Exception("Такого пути не существует")
        try:
            urllib.request.urlopen(self.link)
        except URLError:
            log.info('URL does not exist')
            raise Exception('URL does not exist')
        if self.thread_amount <= 0:
            log.info('Thread count cannot be less than one')
            raise Exception('Потоков не может быть меньше одного')

    def _create_threads(self):
        """Создание потоков"""
        for i in range(self.thread_amount):
            thread = downloader.Downloader(self.path, self.saved_links)
            self.threads.append(thread)

    def _start_threads(self):
        """Запускает потоки"""
        for thread in self.threads:
            thread.start()

    def saving_complete(self):
        log = logging.getLogger('WebCrawler.crawler.saving_complete')
        for thread in self.threads:
            thread.join()
        log.info('Downloading is completed')
