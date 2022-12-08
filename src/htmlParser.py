from bs4 import BeautifulSoup
import requests
import re
import nltk
from nltk.corpus import stopwords

# Function to separate the links and text from the rest of the html
class htmlParser:
    def __init__(self,html_content):
        self.content = html_content
        self.soup = BeautifulSoup(self.content,'html.parser')
        self.links = []
        self.words = []
    

    def getLinks(self):
        for link in self.soup.find_all('a',attrs={'href': re.compile("^https://")}):
            self.links.append(link['href'])
        
        return self.links
        
    
    # Function to remove stopwords
    def removeStopWords(self,text):
        stop_words = set(stopwords.words('english'))
        stop_words.update(['\n','\t'])

        words = text.split()

        filtered_sentence = []
        for w in words:
            if w.lower() not in stop_words:
                filtered_sentence.append(w)

        return filtered_sentence

    
    def getWords(self):
        text = self.soup.get_text()
        self.words = self.removeStopWords(text)

        return self.words

        





    




