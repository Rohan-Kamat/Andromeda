#!/usr/bin/python
import threading
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import sys
import pickle
import click
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from _parser import Parser

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

INITIAL_LINKS = [
    'https://www.wikipedia.org/'
]
link_queue=Queue()
for link in INITIAL_LINKS:
    link_queue.put(link) 
 
class Crawler:
    def __init__(self, chromedriver_path=CHROMEDRIVER_PATH):
        self.parser = Parser()
        
        # self.pool = ThreadPoolExecutor(max_workers=2)
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
         global link_queue
         link_queue.put(url)
         return 
    #def run_thread
    def run(self,id,lock):
         print("Crawler id:",id)
         global link_queue
         while link_queue.empty(): 
            pass
         while True:
          try:
            link = link_queue.get()
            print(link)
            page=self.get(link)
            lock.acquire()
            new_links, _ = self.parser.parse(link,page)
            for link in new_links:
               link_queue.put(link)
            lock.release()
          except Exception as error:
                 print("Error12 Occurred!")
                 link_queue.put(link)
          print(link_queue.qsize())
         
    def runner(self):
     num_crawlers=2
     crawlers=[]
     lock=threading.Lock()
     for id in range(num_crawlers):
       crawlers.append(threading.Thread(target=self.run,args=(id,lock)))
     for crawler in crawlers:
        crawler.start()
     for crawler in crawlers:
        crawler.join()
@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
def start():
  try:
    crawler = Crawler(
        chromedriver_path=CHROMEDRIVER_PATH)
    crawler.runner()
  except Exception as error:
     print("Error Occurred!")
     start()
     #raise Exception from error   
  
cli.add_command(start)
if __name__ == '__main__':
    cli()