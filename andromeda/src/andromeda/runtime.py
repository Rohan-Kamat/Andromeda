import abc
from threading import Thread
import atexit
import pickle

from andromeda.crawler import Crawler
from andromeda.parser import Parser
from andromeda.config import PROGRESS_FILE


class Runtime(metaclass=abc.ABCMeta):
    def __init__(self, n_workers, link_queue, data_queue, name):
        atexit.register(self.exit_handler)

        self.n_workers = n_workers

        self.link_queue = link_queue
        self.data_queue = data_queue

        self.name = name

        self.workers = [Thread(target=self.worker, name=f'{name}#{worker_id}') for worker_id in range(n_workers)]

    @abc.abstractmethod
    def worker(self):
        """
        """

    @abc.abstractmethod
    def exit_handler(self):
        """
        """

    def start(self):
        for worker in self.workers:
            worker.start()

    def join(self):
        for worker in self.workers:
            worker.join()

class CrawlerRuntime(Runtime):
    def __init__(self, n_workers, link_queue, data_queue):
        super().__init__(n_workers, link_queue, data_queue, 'Crawler')

    def worker(self):
        crawler = Crawler()
        crawler.run(self.link_queue, self.data_queue)

    def exit_handler(self):
        with open(PROGRESS_FILE, 'wb') as save_file:
            pickle.dump(list(self.link_queue.queue), save_file)

class ParserRuntime(Runtime):
    def __init__(self, n_workers, link_queue, data_queue):
        super().__init__(n_workers, link_queue, data_queue, 'Parser')

    def worker(self):
        parser = Parser()
        parser.run(self.data_queue, self.link_queue)

    def exit_handler(self):
        pass
