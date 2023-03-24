import pickle
from queue import Queue
import logging

import click
from bs4 import BeautifulSoup

from andromeda.indexer import Websites, InvertedIndex, Summary
from andromeda.config import PROGRESS_FILE
from andromeda.runtime import CrawlerRuntime, ParserRuntime
from andromeda.crawler import Crawler
from andromeda.parser import Parser


INITIAL_LINKS = [
    'https://www.wikipedia.org'
]
# try:
#     with open(PROGRESS_FILE, 'rb') as save_file:
#         logging.info("Loading INITIAL_LINKS from %s", PROGRESS_FILE)
#         INITIAL_LINKS = pickle.load(save_file)
# except Exception as error:
#     pass

link_queue = Queue()
for link in INITIAL_LINKS:
    link_queue.put(link)
logging.info("Initialising link_queue with INITIAL_LINKS: %s", INITIAL_LINKS)

data_queue = Queue()

@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
@click.option('--n_crawler', type=int, help="Number of crawlers", default=1)
@click.option('--n_parser', type=int, help="Number of parsers", default=1)
def start(n_crawler, n_parser):
    parser = ParserRuntime(n_parser, link_queue, data_queue)
    parser.start()

    crawler = CrawlerRuntime(n_crawler, link_queue, data_queue)
    crawler.start()

    parser.join()
    crawler.join()

@click.command(help="Flush the database")
def flush():
    collections = [Websites(), InvertedIndex(), Summary()]
    for collection in collections:
        collection.flush()

@click.command(help="")
@click.option('--url', type=str, help="URL to be mocked")
def debug(url):
    crawler = Crawler()
    html = crawler.get(url)
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')

    parser = Parser()

    lang = parser.get_language(soup)
    print(lang)

    links = parser.get_links(soup)

    text = soup.get_text()
    print(text)
    word_freq = parser.get_word_frequency(text)
    # print(word_freq)

cli.add_command(start)
cli.add_command(flush)
cli.add_command(debug)

if __name__ == '__main__':
    cli()
