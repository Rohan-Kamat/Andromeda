import pickle
from queue import Queue
import logging
from urllib.parse import urlparse, urljoin

import click
from bs4 import BeautifulSoup

from andromeda.indexer import Websites, InvertedIndex, Summary, Hosts
from andromeda.runtime import CrawlerRuntime, ParserRuntime
from andromeda.crawler import Crawler
from andromeda.parser import Parser


@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
@click.option('--n_crawler', type=int, help="Number of crawlers", default=1)
@click.option('--n_parser', type=int, help="Number of parsers", default=1)
@click.option('--initial_links', type=str, multiple=True, help="Initial list of links to begin crawling", default=['https://www.nitk.ac.in'])
@click.option('--load', is_flag=True, help="Start from where you left")
def start(n_crawler, n_parser, initial_links, load):
    initial_links = list(initial_links)
    try:
        if load:
            websites = Websites()

            uncrawled = websites.get_uncrawled()
            if len(uncrawled):
                initial_links = [obj['url'] for obj in uncrawled]
    except Exception as error:
        logging.error(error)
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
    collections = [Websites(), InvertedIndex(), Summary(), Hosts()]
    for collection in collections:
        collection.flush()

@click.command(help="")
@click.option('--url', type=str, help="URL to be mocked")
def debug(url):
    # pylint: disable=all

    crawler = Crawler()
    html = crawler.get(url)
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')

    parser = Parser()

    lang = parser.get_language(soup)

    parsed_url = urlparse(url)
    # print(parsed_url)
    links = parser.get_links(url, soup)
    print(url)
    # print(links)

    text = soup.get_text()
    # print(text)
    word_freq = parser.get_word_frequency(text)
    print(word_freq)

cli.add_command(start)
cli.add_command(flush)
cli.add_command(debug)

if __name__ == '__main__':
    cli()
