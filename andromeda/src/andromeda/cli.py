import threading

import click

from andromeda.crawler import Crawler
from andromeda.indexer import Websites, InvertedIndex, Summary


def start_crawler(crawler_id):
    crawler = Crawler(crawler_id)
    crawler.run()

@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
@click.option('--n_thread', type=int, help="Number of threads", default=1)
def start(n_thread):
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
