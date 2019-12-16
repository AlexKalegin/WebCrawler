import requests
import os
import threading
import re
import logging
from bs4 import BeautifulSoup

module_log = logging.getLogger('WebCrawler.downloader')


class Downloader(threading.Thread):
    """Класс, сохраняющий содержимое страниц"""
    def __init__(self, path, saved_links):
        threading.Thread.__init__(self)
        self.path = path
        self.saved_links = saved_links
        self.lock = threading.RLock()

    def run(self):
        while True:
            with self.lock:
                if len(self.saved_links) != 0:
                    link = self.saved_links.popleft()
                    self.save_page(link)
                    self.save_pictures(link)

    def save_page(self, link):
        page = requests.get(link).text
        page_name = link.replace("https://", "")
        page_name = re.sub('[^a-zA-Z0-9]', '', page_name)
        log = logging.getLogger('WebCrawler.downloader.save_page')
        if not os.path.exists(os.path.join(self.path, '{}.html'.format(page_name))):
            with open(os.path.join(self.path, 'pages', '{}.html'.format(page_name)), 'w', encoding='utf8`') as file:
                file.write(page)
                log.info('Page was loaded: {}'.format(link))
        else:
            logging.info('File {} has been already downloaded'.format(page_name))

    def save_pictures(self, link):
        response = requests.get(link).text
        soup = BeautifulSoup(response, 'html.parser')
        pictures = soup.findAll('img')
        for picture in pictures:
            pic = picture['src']
            img = requests.get(pic).content
            picture_name = pic[pic.rfind('/')+1:pic.rfind('?')]
            with open(os.path.join(self.path, 'images', '{}'.format(picture_name)), 'wb') as image:
                image.write(img)
