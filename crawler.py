import click
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@click.group()
def cli():
    pass


# Ex command to run this function
#  python3 crawler.py crawler <URL>
@click.command()
@click.argument("url" , help = "The URL to start the crawler") 
def crawler(url):
    print("Starting the crawler")
    print(url)
    options = Options()
    # Enabling the headless header will make the crawler run in background
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Crawling throught the site
    driver.get(url)

    # Finding all the elements by Tag name = a
    elements = driver.find_elements(By.TAG_NAME, "a")
    
    print(f"There are {len(elements)} links on this page")

    for a in elements:
        print(a.get_attribute("href"))

    print("Crawler ended")


@click.command()
def test():
    print("This is a test function")

cli.add_command(crawler)
cli.add_command(test)


if __name__ == '__main__':
    cli()