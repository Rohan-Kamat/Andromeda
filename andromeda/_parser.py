from urllib.parse import urlparse, urljoin
import sys
import re

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

from indexer import Indexer
sys.path.append('../')

class Parser:
    def __init__(self):
        self.indexer = Indexer()

    @staticmethod
    def __get_links(soup):
        # print("iukjb")
        links = []
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            url = link['href']
            links.append(urljoin(url, urlparse(url).path))
        # print("links size : ",(links))
        return links

    @staticmethod
    def __get_word_frequency(soup,t,self):
        try:
            text = soup.get_text()
            #Regular expression for replacing string of numbers with an empty string
            text = re.sub(r'\b\d+\b', '', text)
            vectorizer = CountVectorizer(stop_words='english')
            matrix = vectorizer.fit_transform([text])
            word_freq = pd.DataFrame(
                matrix.toarray(),
                columns=vectorizer.get_feature_names_out()
                ).to_dict('dict')
            doc_length=0
            dict1=dict()
            for word in word_freq:
                doc_length+=word_freq[word][0]
            print("doc length ",doc_length)
            for word in word_freq:
                dict1[word]=[word_freq[word][0],doc_length]
            word_freq = {word: stats[0] for word, stats in word_freq.items()}
            # print("hello ",word_freq ," \n\n\n\n",dict1)
            return word_freq,dict1
        except:
            # if(t<5):
            #     self.__get_word_frequency(soup,t+1) 
            # else:
            return {},{}
    def parse(self, url, html):
        if not self.indexer.exists(url):
            self.indexer.insert_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        links = self.__get_links(soup)
        word_freq,dict1 = self.__get_word_frequency(soup,0,self)  
        new_links = []
        print("New links found ",len(links))
        for link in links:
            refs = self.indexer.increment_num_references(link)
            print(link,refs)
            if refs == 1:
                new_links.append(link)
    
        self.indexer.insert_data(url, word_freq)
        self.indexer.insert_word_data(url,dict1)
        return new_links, word_freq
