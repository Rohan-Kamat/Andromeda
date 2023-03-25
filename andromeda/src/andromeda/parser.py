from urllib.parse import urlparse, urljoin
import re
import logging

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from nltk.stem import PorterStemmer

from andromeda.indexer import Websites, Summary


logger = logging.getLogger(__name__)

class Parser:
    def __init__(self):
        self.websites = Websites()
        self.summary = Summary()

        self.porter_stemmer = PorterStemmer()

    def get_links(self, soup):
        links = set()
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            url = link['href']
            links.add(urljoin(url, urlparse(url).path).strip('/'))
        return list(links)

    def __is_valid(self, word: str) -> bool:
        # Must contain only alphabets and digits
        pattern = re.compile('^[a-zA-Z0-9]+$')
        if not pattern.match(word):
            return False

        # Must contain atleast one alphabet
        if re.search('[a-zA-Z]', word) is None:
            return False

        return True

    def get_word_frequency(self, text):
        vectorizer = CountVectorizer(stop_words='english')
        matrix = vectorizer.fit_transform([text])
        data_frame = pd.DataFrame(
            matrix.toarray(),
            columns=vectorizer.get_feature_names_out()
        ).to_dict('dict')
        word_freq = {self.porter_stemmer.stem(str(word)): stats[0] for word, stats in data_frame.items() if self.__is_valid(word)}
        return word_freq

    def get_language(self, soup):
        try:
            lang = soup.html['lang']
            return lang
        except Exception as error:
            logging.debug(error)
            return None

    def run(self, data_queue, link_queue):
        while True:
            try:
                logging.info("Waiting for page")
                (url, html) = data_queue.get()

                logging.info("Parsing %s", url)
                soup = BeautifulSoup(html, 'html.parser')

                lang = self.get_language(soup)
                if lang is None or 'en' not in lang:
                    self.summary.increment('non_english')
                    continue

                if not self.websites.exists(url):
                    self.websites.insert_url(url)

                links = self.get_links(soup)

                text = soup.get_text()
                word_freq = self.get_word_frequency(text)

                new_links = []
                for link in links:
                    refs = self.websites.increment_num_references(link)
                    if refs == 1:
                        new_links.append(link)

                self.websites.insert_data(url, word_freq, lang)

                for new_link in new_links:
                    link_queue.put(new_link)
                logging.info("The global link_queue has %i url(s)", link_queue.qsize())
                self.summary.increment('parsed')
            except Exception as error:
                logging.error("Failed to parse %s: %s", url, str(error).split('\n', maxsplit=1)[0])
                logging.debug(error)

                link_queue.put(url)
