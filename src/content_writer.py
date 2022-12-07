from bs4 import BeautifulSoup
import requests
from htmlParser import htmlParser


url = "https://palletsprojects.com/p/click/"

r = requests.get(url)
html_content = r.content

parser = htmlParser(html_content)
f = open("../assets/html_content.txt",'w')
f.write(str(parser.soup))
