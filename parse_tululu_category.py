import requests
from bs4 import BeautifulSoup
import lxml
from urllib.parse import urljoin
import logging
from utils import make_soup


def get_book_href(href_block, domain):
    try:
        href = href_block.select_one('a').get('href')
        book_href = urljoin(domain, href)
        return book_href
    except (TypeError, AttributeError):
        return

def get_category_hrefs(soup, domain):
    category_hrefs = list()
    try:
        href_blocks = soup.select('table.d_book')
        for href_block in href_blocks:
            category_hrefs.append(get_book_href(href_block, domain))
        return category_hrefs
    except (TypeError, AttributeError):
        return


logging.basicConfig(level=logging.INFO)
domain = r"http://tululu.org/"

category_hrefs = list()

for page in range(1, 11):
    logging.info(f'process with page № {page}')
    page_category_link = f"{domain}/l55/{page}"
    category_hrefs.extend(get_category_hrefs(make_soup(page_category_link), domain))


print(category_hrefs)
print(len(category_hrefs))
