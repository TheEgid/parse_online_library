import requests
import os
import logging
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from utils import get_path, convert_to_jpg, make_soup, make_imageresize


import pprint
def get_category_hrefs(soup):
    try:
        table = soup.find_all('table', class_='d_book')
        pprint.pprint(table)
        return
    except (TypeError, AttributeError):
        return


def get_book_href(soup, domain):
    try:
        table = soup.find('table', class_='d_book')
        href = table.find('a').get('href')
        book_href = urljoin(domain, href)
        return book_href
    except (TypeError, AttributeError):
        return


domain = r"http://tululu.org/"
g_link = f"{domain}/l55/"
soup = make_soup(g_link)

get_category_hrefs(soup)
#print(get_book_href(soup, domain))