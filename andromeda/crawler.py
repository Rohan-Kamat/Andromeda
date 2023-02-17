#!/usr/bin/python

from queue import Queue
import sys
from threading import Thread

import click
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from _parser import Parser


CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
]

link_queue = Queue()
for link in INITIAL_LINKS:
    link_queue.put(link)

def thread(id):
    crawler = Crawler(id)

    crawler.run()

class Crawler:
    def log(self, msg):
        print(f"Crawler {self.id}: {msg}")

    def __init__(self, id, chromedriver_path=CHROMEDRIVER_PATH):
        global link_queue

        self.id = id

        self.parser = Parser()

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

        self.log("Initialized")

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self):
        while link_queue.empty():
            self.log("Waiting for link")
            pass

        while True:
            link = link_queue.get()

            self.log(f"Getting {link}")

            page = self.get(link)

            new_links, _ = self.parser.parse(link, page)
            for link in new_links:
                link_queue.put(link)
            print(f"The gloabl link_queue has {link_queue.qsize()} links")

            # if link_queue.empty():
            #     sys.exit(0)


@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
def start():
    NUM_CRAWLERS = 2

    crawlers = [Thread(target=thread, args=(id,)) for id in range(NUM_CRAWLERS)]

    for crawler in crawlers:
        crawler.start()

    for crawler in crawlers:
        crawler.join()

cli.add_command(start)

if __name__ == '__main__':
    cli()
