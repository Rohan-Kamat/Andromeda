#!/usr/bin/python

from queue import Queue
import sys
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
    def __init__(self, id, chromedriver_path=CHROMEDRIVER_PATH):
        self.id = id

        self.parser = Parser()

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

        global link_queue

    def log(self, msg):
        print(f"Crawler {self.id}: {msg}")

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self):
        while True:
            link = link_queue.get()
            self.log(f"Getting {link}")

            page = self.get(link)

            new_links, _ = self.parser.parse(link, page)
            for link in new_links:
                link_queue.put(link)

def start_crawler(id):
    print(f"Starting Crawler#{id}")
    crawler = Crawler(id)
    crawler.run()

@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
@click.option('--n_thread', type=int, help="Number of threads")
def start(n_thread):
    threads = [threading.Thread(target=start_crawler, args=(id,)) for id in range(n_thread)]

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
