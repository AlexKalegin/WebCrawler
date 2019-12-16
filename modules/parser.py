import requests
from bs4 import BeautifulSoup


class Parser:
    """Класс, для того, чтобы находить все ссылки с заданного сайта"""
    def __init__(self, link, all_links, saved_links, links, robots):
        self.link = link
        self.all_links = all_links
        self.saved_links = saved_links
        self.links = links
        self.robots = robots

    def save_links(self):
        """Находит и сохраняет все имеющиеся уникальные ссылки"""
        page = requests.get(self.link).text
        soup = BeautifulSoup(page, 'html.parser')
        links_on_page = soup.findAll(href=True)
        for link in links_on_page:
            link = link['href']
            link = self.make_link_correct(link)
            if link not in self.all_links:
                if link.startswith(self.link):
                    if self.robots.can_fetch('*', link):
                        self.all_links.append(link)
                        self.saved_links.append(link)
                        self.links.append(link)

    def make_link_correct(self, link):
        """Делает верный формат ссылок"""
        if not link.startswith('https'):
            if link[0] != "/":
                link = '/' + link
            return self.link + link
        return link
