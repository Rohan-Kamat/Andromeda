import json
import os
import logging
import abc

from bson.json_util import dumps
import pymongo


logger = logging.getLogger(__name__)

class Database(metaclass=abc.ABCMeta):
    def __init__(
            self,
            collection,
            user='admin',
            passwd='adminpw',
            host=os.environ.get('MONGODB_HOST') or 'localhost',
            port=27017,
            database='test',
    ):
        try:
            self.client = pymongo.MongoClient(f'mongodb://{user}:{passwd}@{host}:{port}')
            self.database = self.client[database]
            self.collection = self.database[collection]
            logging.info("%s database connection established!", collection)
        except Exception as error:
            raise Exception from error

    def count(self):
        return self.collection.count_documents({})

    def flush(self) -> None:
        try:
            self.collection.drop()
        except Exception as error:
            logging.error("Unable to flush database: %s", error)

    def exists(self, key: str) -> bool:
        data = self.get(key)
        return data is not None

    @abc.abstractmethod
    def get(self, key: str):
        """
        """

class Summary(Database):
    def __init__(self):
        super().__init__('summary')

    def get(self, key: str):
        data = json.loads(dumps(self.collection.find(
            {'key': key},
            {}
        )))
        assert len(data) <= 1
        return data[0]['value'] if len(data) == 1 else None

    def update(self, key, value):
        if not self.exists(key):
            self.collection.insert_one({
                'key': key,
                'value': 0,
            })

        self.collection.update_one(
            {'key': key},
            {'$set': {'value': value}}
        )

class InvertedIndex(Database):
    def __init__(self):
        super().__init__('inverted_index')

    def get(self, key: str):
        data = json.loads(dumps(self.collection.find(
            {'word': key},
            {}
        )))
        assert len(data) <= 1
        return data[0] if len(data) == 1 else None

    def insert_word(self, word):
        if not self.exists(word):
            self.collection.insert_one({
                'word': word,
                'index': [],
            })

    def update_index(self, word, url, freq):
        self.insert_word(word)

        self.collection.update_one(
            {'word': word},
            {'$push': {'index': (url, freq)}}
        )

class Websites(Database):
    def __init__(self):
        self.index = InvertedIndex()
        self.summary = Summary()

        super().__init__('websites')

    def get(self, key: str):
        data = json.loads(dumps(self.collection.find(
            {'url': key},
            {}
        )))
        assert len(data) <= 1
        return data[0] if len(data) == 1 else None

    def increment_num_references(self, url: str) -> bool:
        if not self.exists(url):
            self.insert_url(url)
        self.collection.update_one(
            {'url': url},
            {'$inc': {'references': 1}}
        )
        return self.get(url)['references']

    def insert_url(self, url: str):
        if not self.exists(url):
            self.collection.insert_one({
                'url': url,
                'references': 0,
                'data': None,
                'crawled': False,
            })

    def insert_data(self, url: str, data: dict, lang: str):
        for word, freq in data.items():
            self.index.update_index(word, url, freq)

        length = sum(data.values())
        total_length = self.summary.get('total_length') or 0
        total_length += length
        self.summary.update('total_length', total_length)

        assert self.exists(url)
        self.collection.update_one(
            {'url': url},
            {'$set': {'data': data, 'crawled': True, 'lang': lang, 'length': length}}
        )
        return self.get(url)
