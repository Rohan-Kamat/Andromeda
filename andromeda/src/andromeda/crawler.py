#!/usr/bin/python

import logging
import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from andromeda.config import LOG_FILE, DOWNLOAD_DIRECTORY, MAXIMUM_RETRIES, DATABASE
from andromeda.indexer import Summary


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f'{LOG_FILE}.{DATABASE}.log',
    filemode='w+',
    format='%(asctime)s %(msecs)d %(pathname)s %(threadName)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

class Crawler:
    def __init__(self, chromedriver_path=CHROMEDRIVER_PATH):
        try:
            shutil.rmtree(DOWNLOAD_DIRECTORY)
        except Exception as error:
            logging.info("Unable to delete %s", DOWNLOAD_DIRECTORY)
            logging.error(error)

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        prefs = {
            'download': {
                'default_directory': os.path.join(os.path.dirname(__file__), DOWNLOAD_DIRECTORY),
                'open_pdf_in_system_reader': False,
                'prompt_for_download': False,
            },
            'plugins': {
                'always_open_pdf_externally': False,
            },
            'download_restrictions': 3
        }
        options.add_experimental_option(
            'prefs', prefs
        )

        self.driver = webdriver.Chrome(options=options, service=Service(chromedriver_path))
        self.driver.set_page_load_timeout(30)

        self.summary = Summary()

        logging.info("Initalised")

    def get(self, url: str):
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def run(self, link_queue, data_queue):
        while True:
            logging.info("Waiting for a URL")
            (get_link, retries) = link_queue.get()
            logging.info("Getting %s", get_link)

            try:
                page = self.get(get_link)
                logging.info("Downloaded %s", get_link)

                data_queue.put((get_link, page))
                self.summary.increment('crawled')
            except Exception as error:
                logging.error("Failed to get %s: %s", get_link, str(error).split('\n', maxsplit=1)[0])
                print(error)

                if retries < MAXIMUM_RETRIES:
                    link_queue.put((get_link, retries + 1))
