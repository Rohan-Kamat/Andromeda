#!/usr/bin/python

import click
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from queue import Queue

from parser import Parser
from indexer import Indexer

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
]

class Crawler:
    def __init__(self, chromedriver_path=CHROMEDRIVER_PATH, initial_links=INITIAL_LINKS):
        self.parser = Parser()

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

        indexer = Indexer()

        self.link_queue = Queue()
        link_queue = Queue()
        for link in initial_links:
            self.link_queue.put(link)
            indexer.insert_url(link)

    def get(self, url:str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self):
        while True:
            link = self.link_queue.get()
            print(link)

            page = self.get(link)

            new_links, _ = self.parser.parse(link, page)
            for link in new_links:
                self.link_queue.put(link)
            print(self.link_queue.qsize())

            if self.link_queue.empty():
                exit(0)

crawler = Crawler()

@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
def start():
    crawler.run()

cli.add_command(start)

if __name__ == '__main__':
    cli()
