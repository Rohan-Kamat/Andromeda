from queue import Queue
import sys

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

        self.inverted_index = {}
        self.doc_index = {}
        self.next_doc_id = 1

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def add_to_inverted_index(self, words: list, url: str):
        doc_id = self.doc_index.get(url, self.next_doc_id)
        if doc_id == self.next_doc_id:
            self.doc_index[url] = doc_id
            self.next_doc_id += 1

        for word in words:
            if word not in self.inverted_index:
                self.inverted_index[word] = {}

            if doc_id not in self.inverted_index[word]:
                self.inverted_index[word][doc_id] = 0

            self.inverted_index[word][doc_id] += 1



    def run(self):
        while True:
            link = self.link_queue.get()
            print(link)

            page = self.get(link)

            new_links, words = self.parser.parse(link, page)
            self.add_to_inverted_index(words, link)

            for new_link in new_links:
                self.link_queue.put(new_link)

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
    print(crawler.inverted_index)


cli.add_command(start)

if __name__ == '__main__':
    cli()


