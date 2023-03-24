#!/usr/bin/python

import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from andromeda.config import LOG_FILE


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    filemode='w+',
    format='%(asctime)s %(msecs)d %(pathname)s %(threadName)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

class Crawler:
    def __init__(self, chromedriver_path=CHROMEDRIVER_PATH):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

        logging.info("Initalised")

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self, link_queue, data_queue):
        while True:
            try:
                logging.info("Waiting for a URL")
                get_link = link_queue.get()
                logging.info("Getting %s", get_link)

                page = self.get(get_link)
                logging.info("Downloaded %s", get_link)

                data_queue.put((get_link, page))
            except Exception as error:
                logging.error("Failed to get %s: %s", get_link, str(error).split('\n', maxsplit=1)[0])
                logging.debug(error)

                link_queue.put(get_link)
