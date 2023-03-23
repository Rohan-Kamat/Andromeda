import json
import os
import logging

from bson.json_util import dumps
import pymongo


logger = logging.getLogger(__name__)

class Indexer:
    def __init__(
            self,
            user='admin',
            passwd='adminpw',
            host=os.environ.get('MONGODB_HOST') or 'localhost',
            port=27017,
            database='test',
    ):
        try:
            logging.info("Initializing DB connection...")
            self.client = pymongo.MongoClient(f'mongodb://{user}:{passwd}@{host}:{port}')
            self.database = self.client[database]
            self.websites = self.database['websites']
            logging.info("DB connection established!")
        except Exception as error:
            raise Exception from error

    def exists(self, url: str) -> bool:
        website = self.get(url)
        return website is not None

    def get(self, url: str):
        website = json.loads(dumps(self.websites.find(
            {'url': url},
            {}
        )))
        assert len(website) <= 1
        return website[0] if len(website) == 1 else None

    def increment_num_references(self, url: str) -> bool:
        if not self.exists(url):
            self.insert_url(url)
        self.websites.update_one(
            {'url': url},
            {'$inc': {'references': 1}}
        )
        return self.get(url)['references']

    def flush(self) -> None:
        try:
            self.websites.drop()
        except Exception as err:
            logging.error("Unable to flush database: %s", err)

    def insert_url(self, url: str):
        if not self.exists(url):
            self.websites.insert_one({
                'url': url,
                'references': 0,
                'data': None,
                'crawled': False,
            })

    def insert_data(self, url: str, data: dict, lang: str):
        assert self.exists(url)
        self.websites.update_one(
            {'url': url},
            {'$set': {'data': data, 'crawled': True, 'lang': lang}}
        )
        return self.get(url)
