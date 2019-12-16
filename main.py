import argparse
from modules import crawler as c
import logging


def main():
    """Метод для ввода пользователем домена, пути, куда сохранять страницы, и количество потоков"""
    descr = 'Программа, для сохранения страниц. Просто введите домен и путь, ' \
            'куда сохранять '
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('--link', type=str,
                        required=True, help='Какая ссылка?')
    parser.add_argument('--path', type=str, required=True,
                        help='Куда сохранять?')
    parser.add_argument('--threads', type=int, required=True, default=1,
                        help='Сколько потоков должно работать?')
    args = parser.parse_args()
    log = logging.getLogger('WebCrawler')
    log.setLevel(logging.INFO)
    fh = logging.FileHandler('loaded_pages.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    log.info('Program started')
    crawler = c.Crawler(args.link, args.path, args.threads)
    crawler.start()


if __name__ == '__main__':
    main()

