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


@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
@click.option('--n_crawler', type=int, help="Number of crawlers", default=1)
@click.option('--n_parser', type=int, help="Number of parsers", default=1)
@click.option('--initial_links', type=str, multiple=True, help="Initial list of links to begin crawling", default=['https://www.wikipedia.org'])
def start(n_crawler, n_parser, initial_links):
    initial_links = list(initial_links)
    # try:
    #     with open(PROGRESS_FILE, 'rb') as save_file:
    #         logging.info("Loading INITIAL_LINKS from %s", PROGRESS_FILE)
    #         INITIAL_LINKS = pickle.load(save_file)
    # except Exception as error:
    #     pass
    logging.info("Initialising link_queue with INITIAL_LINKS: %s", initial_links)

    link_queue = Queue()
    for link in initial_links:
        link_queue.put((link, 0))

    data_queue = Queue()

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

    links = parser.get_links(soup)

    text = soup.get_text()
    word_freq = parser.get_word_frequency(text)
    print(word_freq)

    print(parser.get_links(soup))

cli.add_command(start)
cli.add_command(flush)
cli.add_command(debug)

if __name__ == '__main__':
    cli()
