from bs4 import BeautifulSoup
import requests
import re
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


# Function to separate the links and text from the rest of the html
class htmlParser:
    def __init__(self, html_content):
        self.content = html_content
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.links = []
        self.word_freq = None

    def getLinks(self):
        for link in self.soup.find_all(
            'a', attrs={
                'href': re.compile("^https://")}):
            self.links.append(link['href'])

        return self.links

    def getWordFrequency(self):
        text = self.soup.get_text()

        cv = CountVectorizer(stop_words='english')
        cv_matrix = cv.fit_transform([text])
        # create document term matrix
        self.word_freq = pd.DataFrame(
            cv_matrix.toarray(),
            columns=cv.get_feature_names_out())

        return self.word_freq
