#!/usr/bin/python

from queue import Queue
import threading
import logging

import click
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from ._parser import Parser
from .indexer import Websites


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='andromeda.log',
    filemode='w+',
    format='%(asctime)s %(msecs)d %(pathname)s %(threadName)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
]
link_queue = Queue()
for link in INITIAL_LINKS:
    link_queue.put(link)
logging.info("Initialising link_queue with INITIAL_LINKS: %s", INITIAL_LINKS)

class Crawler:
    def __init__(self, crawler_id, chromedriver_path=CHROMEDRIVER_PATH):
        self.crawler_id = crawler_id

        self.parser = Parser()

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

        logging.info("Initalised")

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self):
        while True:
            get_link = link_queue.get()
            logging.info("The global link_queue has %i url(s)", link_queue.qsize())
            logging.info("Getting %s", get_link)

            page = self.get(get_link)
            logging.info("Downloaded %s", get_link)

            new_links, _ = self.parser.parse(get_link, page)
            for new_link in new_links:
                link_queue.put(new_link)

def start_crawler(crawler_id):
    crawler = Crawler(crawler_id)
    crawler.run()

@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
@click.option('--n_thread', type=int, help="Number of threads", default=1)
def start(n_thread):
    threads = [threading.Thread(target=start_crawler, args=(crawler_id,), name=f'Crawler#{crawler_id}') for crawler_id in range(n_thread)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

@click.command(help="Get a single link")
@click.option('--url', type=str, help="URL to be crawled")
def get(url):
    crawler = Crawler(0)
    crawler.get(url)

@click.command(help="Flush the database")
def flush():
    logging.info("Flushing the database")
    websites = Websites()
    websites.flush()

cli.add_command(start)
cli.add_command(flush)
cli.add_command(get)


if __name__ == '__main__':
    cli()
