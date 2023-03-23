import os
import math
import abc

from .indexer import InvertedIndex
from ._parser import Parser


class Ranker(metaclass=abc.ABCMeta):
    def __init__(self):
        self.index = InvertedIndex()
        self.parser = Parser()

class BM25(Ranker):
    def get_documents(self, query):
        word_freq = self.parser.get_word_frequency(query)

        return []
