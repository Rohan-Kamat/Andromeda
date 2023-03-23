import json
import os

from bson.json_util import dumps
import pymongo
import redis

class Indexer:
    def __init__(
            self,
            user='admin',
            passwd='adminpw',
            host=os.environ.get('MONGODB_HOST') or 'localhost',
            port=27017,
            database='test',
    ):
        print("host",host)
        try:
            self.cache = redis.Redis( host='localhost', port=6379,db=0,password=None,decode_responses=True)
            if self.cache.ping():
                print("Redis DB has established!")
            print("Initializing DB connection...")
            self.client = pymongo.MongoClient(f'mongodb://{user}:{passwd}@{host}:{port}')
            self.database = self.client[database]
            self.websites = self.database['websites']
            self.index = self.database['index']
            print("DB connection established!")

        except Exception as error:
            raise Exception from error

    def exists(self, url: str) -> bool:
         print("Checking exists",self.cache.get(url),"here")
         website = self.get(url)
        #  print(website)
         return website is not None
    def word_exists(self, word: str) -> bool:
        word_dat = self.word_get(word)
        return word_dat is not None
    def word_get(self, word: str):
       word_dat = json.loads(dumps(self.index.find(
            {'word': word},
            {}
        ))) 
       if(word_dat==[]):
         return None
       else:
        return word_dat
    def insert_word(self, word: str):
        if not self.word_exists(word):
            self.index.insert_one({
                'word': word,
                'location': []
            })

    def update_word(self, word: str,url :str,ref)-> bool:
     if not self.word_exists(word):
         self.insert_word(word)
     self.index.update_one({'word':word},{'$push':{'location':[url,ref]}})


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
            
        self.cache.set(url,'False1')
        self.websites.update_one(
            {'url': url},
            {'$inc': {'references': 1}}
        )
        
        print("References", self.websites.find_one({"url":url})['references'])
        return self.websites.find_one({"url":url})['references']
    
    def crawler_checker(self, url: str):
        return self.get(url)['crawled']
        
    def insert_url(self, url: str):
        #print("Checking insert url",self.cache.exists(url),"here")
        if not self.exists(url):
            print("Inserting url ",url)
            print(self.websites.find_one({'url':url}))
            self.websites.insert_one({
                'url': url,
                'references': 0,
                'data': None,
                'crawled': False
            })
    
    def insert_data(self, url: str, data: dict):
        assert self.exists(url)
        self.websites.update_one(
            {'url': url},
            {'$set': {'data': data, 'crawled': True}}
        )
        return self.get(url)
    def insert_word_data(self,url:str,data:dict):
     for word in data:
        self.update_word(word,url,data[word])