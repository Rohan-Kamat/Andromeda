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
        links = []
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            url = link['href']
            links.append(urljoin(url, urlparse(url).path))
        return links

    @staticmethod
    def __get_word_frequency(soup):
        text = soup.get_text()
        vectorizer = CountVectorizer(stop_words='english')
        matrix = vectorizer.fit_transform([text])
        word_freq = pd.DataFrame(
            matrix.toarray(),
            columns=vectorizer.get_feature_names_out()
        ).to_dict('dict')
        word_freq = {word: stats[0] for word, stats in word_freq.items()}
        return word_freq

    def parse(self, url, html):
        if not self.indexer.exists(url):
            self.indexer.insert_url(url)

        soup = BeautifulSoup(html, 'html.parser')

        links = Parser.__get_links(soup)

        word_freq = Parser.__get_word_frequency(soup)

        new_links = []
        for link in links:
            refs = self.indexer.increment_num_references(link)
            if refs == 1:
                new_links.append(link)

        self.indexer.insert_data(url, word_freq)

        return new_links, word_freq
