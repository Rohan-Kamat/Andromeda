from urllib.parse import urlparse, urljoin
import re
import logging

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from nltk.stem import PorterStemmer

from indexer import Indexer


logger = logging.getLogger(__name__)

class Parser:
    def __init__(self):
        self.indexer = Indexer()

        self.porter_stemmer = PorterStemmer()

    def __get_links(self, soup):
        links = []
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            url = link['href']
            links.append(urljoin(url, urlparse(url).path))
        return links

    def __is_valid(self, word: str) -> bool:
        # Must contain only alphabets and digits
        pattern = re.compile('^[a-zA-Z0-9]+$')
        if not pattern.match(word):
            return False

        # Must contain atleast one alphabet
        if re.search('[a-zA-Z]', word) is None:
            return False

        return True

    def __get_word_frequency(self, soup):
        text = soup.get_text()
        # Remove stop words
        vectorizer = CountVectorizer(stop_words='english')
        matrix = vectorizer.fit_transform([text])
        word_freq = pd.DataFrame(
            matrix.toarray(),
            columns=vectorizer.get_feature_names_out()
        ).to_dict('dict')
        word_freq = {self.porter_stemmer.stem(str(word)): stats[0] for word, stats in word_freq.items() if self.__is_valid(word)}
        return word_freq

    def __get_language(self, soup):
        try:
            lang = soup.html['lang']
            return lang
        except Exception as err:
            logging.error("Language 404: %s", err)
            return None

    def parse(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')

        lang = self.__get_language(soup)
        if lang is None or 'en' not in lang:
            return [], {}

        if not self.indexer.exists(url):
            self.indexer.insert_url(url)

        links = self.__get_links(soup)

        word_freq = self.__get_word_frequency(soup)

        new_links = []
        for link in links:
            refs = self.indexer.increment_num_references(link)
            if refs == 1:
                new_links.append(link)

        self.indexer.insert_data(url, word_freq, lang)

        logging.info("Parsed %s", url)

        return new_links, word_freq
