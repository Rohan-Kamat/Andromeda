import json
import os
import logging
import abc

from bson.json_util import dumps
import pymongo

from andromeda.config import FREQUENCY_THRESHOLD


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

class Hosts(Database):
    def __init__(self):
        super().__init__('hosts')

        self.collection.create_index('host', unique=True)
    
    def get(self, key: str):
        data = json.loads(dumps(self.collection.find(
            {'host': key},
            {}
        )))
        return data[0]['value'] if len(data) == 1 else None

    def add(self, host):
        self.collection.update_one(
            {'host': host},
            {'$set': {'host': host}},
            upsert=True
        )

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

    def add(self, key, value=0):
        self.collection.update_one(
            {'key': key},
            {'$set': {'value': value}},
            upsert=True
        )

    def update(self, key, value):
        self.collection.update_one(
            {'key': key},
            {'$set': {'value': value}},
            upsert=True
        )

    def increment(self, key):
        self.collection.update_one(
            {'key': key},
            {'$inc': {'value': 1}},
            upsert=True
        )

class InvertedIndex(Database):
    def __init__(self):
        super().__init__('inverted_index')

        self.collection.create_index('word', unique=True)

    def get(self, key: str):
        data = json.loads(dumps(self.collection.find(
            {'word': key},
            {}
        )))
        assert len(data) <= 1
        return data[0] if len(data) == 1 else None

    def insert_word(self, word):
        self.collection.update_one(
            {'word': word},
            {'$set': {'index': []}},
            upsert=True
        )

    def update_index(self, word, url, freq):
        self.insert_word(word)

        self.collection.update_one(
            {'word': word},
            {'$push': {'index': (url, freq)}}
        )

class Websites(Database):
    def __init__(self):
        super().__init__('websites')

        self.index = InvertedIndex()
        self.summary = Summary()

        self.collection.create_index('url', unique=True)

    def get(self, key: str):
        data = json.loads(dumps(self.collection.find(
            {'url': key},
            {}
        )))
        return data[0] if len(data) == 1 else None

    def increment_num_references(self, url: str) -> bool:
        self.collection.update_one(
            {'url': url},
            {'$inc': {'references': 1}},
            upsert=True
        )
        return self.get(url)['references']

    def insert_url(self, url: str):
        self.collection.update_one(
            {'url': url},
            {'$set': {'references': 0}},
            upsert=True
        )

    def insert_data(self, url: str, data: dict, lang: str):
        length = 0
        for word, freq in data.items():
            length += freq
            if freq > FREQUENCY_THRESHOLD:
                self.index.update_index(word, url, freq)

        total_length = self.summary.get('total_length') or 0
        total_length += length
        self.summary.update('total_length', total_length)

        assert self.exists(url)
        self.collection.update_one(
            {'url': url},
            {'$set': {'lang': lang, 'length': length}}
        )
        return self.get(url)
