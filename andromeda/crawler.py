#!/usr/bin/python

from bs4 import BeautifulSoup
from queue import Queue
import sys
import requests

import click
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from _parser import Parser


CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
]

class Crawler:
    def __init__(self, chromedriver_path=CHROMEDRIVER_PATH, initial_links=None):
        if initial_links is None:
            initial_links = INITIAL_LINKS

        self.parser = Parser()

        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

        self.link_queue = Queue()
        for link in initial_links:
            self.link_queue.put(link)

    def get(self, url: str):
        self.driver.get(url)
        #content = requests.get(url).content
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        page = self.driver.page_source
        if('en' in soup.html['lang']):
            return page
        else:
            return None
    

    def run(self):
        while True:
            link = self.link_queue.get()
            print(link)
            
            page = self.get(link)
            if(page == None):
                continue

            new_links, _ = self.parser.parse(link, page)
            for link in new_links:
                self.link_queue.put(link)
            print(self.link_queue.qsize())

            if self.link_queue.empty():
                sys.exit(0)


@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
def start():
    crawler = Crawler(
        chromedriver_path=CHROMEDRIVER_PATH,
        initial_links=INITIAL_LINKS
    )
    crawler.run()

cli.add_command(start)

if __name__ == '__main__':
    cli()

