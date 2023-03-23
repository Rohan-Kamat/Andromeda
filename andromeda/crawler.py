#!/usr/bin/python

import threading
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import sys
import pickle
import sys
from queue import Queue
from bs4 import BeautifulSoup
import click
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from _parser import Parser

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
    # 'https://www.nitk.ac.in/'
]
link_queue=Queue()
for link in INITIAL_LINKS:
   link_queue.put(link) 
def run_thread(id):
   crawler = Crawler(
      chromedriver_path=CHROMEDRIVER_PATH)
   crawler.run(id)
class Crawler:
  def __init__(self, chromedriver_path=CHROMEDRIVER_PATH):
    self.parser = Parser()
    global link_queue
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    try:
       self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
    except Exception as error:
       print("Error Occurred!")

  def get(self, url: str):
    try:
      self.driver.get(url)
      page = self.driver.page_source
      return page
    except:
      print("Unable to get the Page!!")
      link_queue.put(url)
      return 
    
  def run(self,id):
    print("Crawler id: ",id," Queue Size  " ,link_queue.qsize())
    while link_queue.empty(): 
      pass
    while True:
       try:
        link = link_queue.get()
        print("parsing the link",link)
        print("link ",link)
        page=self.get(link)
        new_links, _ = self.parser.parse(link,page)
        for link in new_links:
           link_queue.put(link)
        print("THe new links ",new_links)
       except Exception as error:
        print("Error Occurred!")
        link_queue.put(link)
        print("link queue size ",link_queue.qsize())
    
@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
def start():
  try:
    num_crawlers=2
    crawlers=[]
    for id in range(num_crawlers):
      print("id ",id)
      crawlers.append(threading.Thread(target=run_thread,args=(id,)))
    for crawler in crawlers:
        crawler.start()
    for crawler in crawlers:
        crawler.join()
  except Exception as error:
     print("Error Occurred!")
     start()
     #raise Exception from error   
  
cli.add_command(start)
if __name__ == '__main__':
    cli()
