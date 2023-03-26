from urllib.parse import urlparse, urljoin
import re
import logging

from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk

from andromeda.indexer import Websites, Summary, Hosts


logger = logging.getLogger(__name__)

class Parser:
    def __init__(self):
        self.websites = Websites()
        self.summary = Summary()
        self.hosts = Hosts()

        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def get_links(self, soup):
        links = set()
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            url = link['href']
            links.add(urljoin(url, urlparse(url).path).strip('/'))
        return list(links)

    def __is_valid(self, word: str) -> bool:
        if word in self.stop_words:
            return False

        # Must contain only alphabets and digits
        pattern = re.compile('^[a-zA-Z0-9@\-_\.]+$')
        if not pattern.match(word):
            return False

        # Must contain atleast one alphabet
        if re.search('[a-zA-Z]', word) is None:
            return False

        return True

    def get_word_frequency(self, text):
        word_freq = {}
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence):
                word = self.stemmer.stem(word.lower())
                if word not in word_freq:
                    word_freq[word] = 0
                if self.__is_valid(word):
                    word_freq[word] += 1
        return {word: freq for word, freq in word_freq.items() if freq > 0}

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
                    self.websites.insert_data(url, {}, lang)
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
                    link_queue.put((new_link, 0))
                logging.info("The global link_queue has %i url(s)", link_queue.qsize())

                self.hosts.add(urlparse(url).hostname)

                self.summary.increment('parsed')
            except Exception as error:
                logging.error("Failed to parse %s: %s", url, str(error).split('\n', maxsplit=1)[0])
                logging.debug(error)

                # link_queue.put((new_link, 0))
