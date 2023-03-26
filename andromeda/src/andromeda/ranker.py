import math
import abc

from andromeda.indexer import InvertedIndex, Websites, Summary
from andromeda.parser import Parser


class Ranker(metaclass=abc.ABCMeta):
    def __init__(self):
        self.index = InvertedIndex()
        self.websites = Websites()
        self.parser = Parser()
        self.summary = Summary()

class BM25(Ranker):
    def __init__(self, b=0.75, k=1.2):
        self._k = k
        self._b = b

        super().__init__()

    def __sort_docs(self, docs: dict) -> list:
        return sorted(docs, key=docs.get, reverse=True)

    def get_docs(self, query):
        word_freq = self.parser.get_word_frequency(query)

        n_docs = self.websites.count()
        avg_doc_len = self.summary.get('total_length') / n_docs

        docs = {}
        for word, n_query in word_freq.items():
            if not self.index.exists(word):
                continue

            word_index = self.index.get(word)

            doc_freq = len(word_index['index'])
            inv_doc_freq = math.log((n_docs + 1) / doc_freq)

            for [url, n_doc] in word_index['index']:
                doc = self.websites.get(url)

                if 'length' not in doc:
                    continue

                doc_len = doc['length']
                norm_len = 1 - self._b + self._b * doc_len / avg_doc_len

                term_freq = n_doc / norm_len
                term_freq = (self._k + 1) * term_freq / (self._k + term_freq)

                if url not in docs:
                    docs[url] = 0
                docs[url] += n_query * term_freq * inv_doc_freq

        docs = self.__sort_docs(docs)
        return docs
