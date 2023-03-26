from bs4 import BeautifulSoup

from andromeda.crawler import Crawler


def get_text(node):
    return node.text.strip()

def get_metadata(url: str):
    crawler = Crawler()

    try:
        html = crawler.get(url)
    except Exception as error:
        print(error)
        return {'url': url}

    soup = BeautifulSoup(html, 'html.parser')

    title = soup.title.get_text()

    heading = get_text(soup.select('h1')[0])

    description = get_text(soup.select('p')[0])

    return {
        'url': url,
        'title': title,
        'heading': heading,
        'description': description
    }
