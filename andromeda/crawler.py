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


class Crawler:
    def __init__(self, chromedriver_path=CHROMEDRIVER_PATH, initial_links=None):
        if initial_links is None:
            initial_links = INITIAL_LINKS
        self.parser = Parser()
        self.pool = ThreadPoolExecutor(max_workers=2)
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        f=1
        while(f==1):
         try:
          self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
          self.link_queue=Queue()
          for link in initial_links:
            self.link_queue.put(link) 
          f=0
         except Exception as error:
            print("Error Occurred!")
    def get(self, url: str):
        try:
         self.driver.get(url)
         page = self.driver.page_source
         #print(page)
    
         return [page,url]
        except:
         print("Unable to get the Page!!")
         self.link_queue.put(url)
         return []
    # def run_thread(self,l1):
    #      while True:  
    #         link = self.link_queue.get()
    #         print(link)
    #         page = self.get(link)
    #         try:
    #          new_links, _ = self.parser.parse(link, page)
    #          l1.acquire()
    #          for link in new_links:
    #             self.link_queue.put(link)
    #          print(self.link_queue.qsize())
    #          if self.link_queue.empty():
    #             print("Finish!!")
    #             sys.exit(0)
    #          l1.release()
    #         except Exception as error:
    #            print("Error12 Occurred")
    #            self.link_queue.put(link)
      
    # def scrape_page(self, url):
    #    try:
    #          res = requests.get(url, timeout=(3, 30))
    #          return res
    #    except requests.RequestException:
    #          return
    def run_thread(self,job):
     try:
      page=job.result()
      new_links, _ = self.parser.parse(page[1], page[0])
      print(new_links)
      for link in new_links:
          self.link_queue.put(link)
     except Exception as error:
                print("Error13 Occurred!")
    def run(self):
         while True:
          try:
            print("\n Name of the current executing process: ",
                      multiprocessing.current_process().name, '\n')
            link = self.link_queue.get()
            print(link)
            job = self.pool.submit(self.get,link)
           # page = self.get(link)
            job.add_done_callback(self.run_thread)
           # new_links, _ = self.parser.parse(link, page)
           # for link in new_links:
                # self.link_queue.put(link)
          except Exception as error:
                print("Error12 Occurred!")
                self.link_queue.put(link)
          print(self.link_queue.qsize())
          if self.link_queue.empty():
                 print("Finish!!")
                 #sys.exit(0)
    #    l1=threading.Lock()
    #    c1 = threading.Thread(target=self.run_thread,name='c1',args=(l1,))
    #    c2 = threading.Thread(target=self.run_thread,name='c2',args=(l1,))
    #    c1.start()
    #    c2.start()
    #    c1.join()
    #    c2.join()
@click.group()
def cli():
    pass

@click.command(help="Start the crawler")
def start():
  try:
    crawler = Crawler(
        chromedriver_path=CHROMEDRIVER_PATH,
        initial_links=INITIAL_LINKS)
    crawler.run()
  except Exception as error:
     print("Error Occurred!")
     start()
     #raise Exception from error   
  
cli.add_command(start)
if __name__ == '__main__':
    cli()