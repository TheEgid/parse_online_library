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
    category_hrefs = []
    try:
        href_blocks = soup.select('table.d_book')
        for href_block in href_blocks:
            category_hrefs.append(get_book_href(href_block, domain))
        return category_hrefs
    except (TypeError, AttributeError):
        return


def fetch_hrefs(domain, category, amount):
    category_hrefs = []
    for page in range(0, amount):
        logging.info(f'process with page № {page}')
        page_category_link = f"{domain}/{category}/{page}"
        category_hrefs.extend(
            get_category_hrefs(make_soup(page_category_link), domain))
        if len(set(category_hrefs)) == amount:
            break
    return category_hrefs



