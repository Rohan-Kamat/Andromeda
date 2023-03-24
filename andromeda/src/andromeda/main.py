import threading
import atexit
import pickle
from queue import Queue
import logging

import click

from andromeda.crawler import Crawler
from andromeda.indexer import Websites, InvertedIndex, Summary
from andromeda.config import PROGRESS_FILE


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

def start_crawler(crawler_id):
    crawler = Crawler(crawler_id)
    crawler.run(link_queue)

def exit_handler():
    with open(PROGRESS_FILE, 'wb') as save_file:
        pickle.dump(list(link_queue.queue), save_file)


@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
@click.option('--n_thread', type=int, help="Number of threads", default=1)
def start(n_thread):
    atexit.register(exit_handler)

    threads = [threading.Thread(target=start_crawler, args=(crawler_id,), name=f'Crawler#{crawler_id}') for crawler_id in range(n_thread)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    

@click.command(help="Flush the database")
def flush():
    websites = Websites()
    websites.flush()

    inverted_index = InvertedIndex()
    inverted_index.flush()

    summary = Summary()
    summary.flush()

cli.add_command(start)
cli.add_command(flush)

if __name__ == '__main__':
    cli()
