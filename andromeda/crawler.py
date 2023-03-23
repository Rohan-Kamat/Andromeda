#!/usr/bin/python

from queue import Queue
import threading

import click
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from _parser import Parser
from indexer import Indexer


CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
]
link_queue = Queue()
for link in INITIAL_LINKS:
    link_queue.put(link)

class Crawler:
    def __init__(self, crawler_id, chromedriver_path=CHROMEDRIVER_PATH):
        self.crawler_id = crawler_id

        self.parser = Parser()

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    def log(self, msg):
        print(f"Crawler {self.crawler_id}: {msg}")

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self):
        while True:
            get_link = link_queue.get()
            self.log(f"Getting {get_link}")

            page = self.get(get_link)

            new_links, _ = self.parser.parse(get_link, page)
            for new_link in new_links:
                link_queue.put(new_link)

def start_crawler(crawler_id):
    print(f"Starting Crawler#{crawler_id}")
    crawler = Crawler(crawler_id)
    crawler.run()

@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
@click.option('--n_thread', type=int, help="Number of threads")
def start(n_thread):
    threads = [threading.Thread(target=start_crawler, args=(crawler_id,)) for crawler_id in range(n_thread)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

@click.command(help="Flush the database")
def flush():
    indexer = Indexer()
    indexer.flush()

cli.add_command(start)
cli.add_command(flush)

if __name__ == '__main__':
    cli()
