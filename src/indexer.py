
import pymongo
from bson.json_util import dumps
import json

class WebsitesDatabaseClient:
    def __init__(
        self,
        user='admin',
        passwd='adminpw',
        host='localhost',
        port=27017,
        db='test',
    ):
        try:
            self.client = pymongo.MongoClient(f'mongodb://{user}:{passwd}@{host}:{port}')
            self.db = self.client[db]
            self.websites = self.db['websites']
            print("Connected to Database!")
        except Exception as error:
            raise ConnectionAbortedError(error)

    def exists(self, url:str) -> bool:
        website = self.get(url)
        return website is not None

    def get(self, url:str):
        website = json.loads(dumps(self.websites.find(
            {'url': url},
            {}
        )))
        assert len(website) <= 1
        return website[0] if len(website) == 1 else None

    def increment_num_references(self, url:str) -> bool:
        if self.exists(url):
            self.websites.update_one(
                {'url': url},
                {'$inc': {'references': 1}}
            )
        else:
            self.websites.insert_one({
                'url': url,
                'references': 1,
                'data': None,
                'crawled': False
            })
        return self.get(url)['crawled']

    def insert_data(self, url:str, data:dict):
        assert self.exists(url)
        self.websites.update_one(
            {'url': url},
            {'$set': {'data': data, 'crawled': True}}
        )
        return self.get(url)