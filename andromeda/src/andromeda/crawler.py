#!/usr/bin/python

from queue import Queue
import logging
import atexit
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from andromeda.parser import Parser
from andromeda.config import LOG_FILE, PROGRESS_FILE


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    filemode='w+',
    format='%(asctime)s %(msecs)d %(pathname)s %(threadName)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
]
try:
    with open(PROGRESS_FILE, 'rb') as save_file:
        logging.info("Loading INITIAL_LINKS from %s", PROGRESS_FILE)
        INITIAL_LINKS = pickle.load(save_file)
except Exception as error:
    pass

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

        atexit.register(exit_handler)
        logging.info("Initalised")

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self):
        while True:
            try:
                get_link = link_queue.get()
                logging.info("The global link_queue has %i url(s)", link_queue.qsize())
                logging.info("Getting %s", get_link)

                page = self.get(get_link)
                logging.info("Downloaded %s", get_link)

                new_links, _ = self.parser.parse(get_link, page)
                for new_link in new_links:
                    link_queue.put(new_link)
            except Exception as error:
                logging.error("Failed to get %s: %s", get_link, str(error).split('\n', maxsplit=1)[0])
                logging.debug(error)

                link_queue.put(get_link)

def exit_handler():
    with open(PROGRESS_FILE, 'wb') as save_file:
        pickle.dump(list(link_queue.queue), save_file)
