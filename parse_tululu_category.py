import requests
import os
import logging
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json
from helpers import get_path, convert_to_jpg, make_soup, make_imageresize
from helpers import get_args_parser
from utils import get_category_hrefs, get_book_title, get_book_author
from utils import get_book_img_src, get_book_comments, get_book_genres


def download_img(url, filepath):
    folder, _ = filepath.split('/')
    response = requests.get(url)
    response.raise_for_status()
    if 'image' not in response.headers['Content-Type']:
        logging.info(f'{url} image passed')
        return
    os.makedirs(folder, exist_ok=True)

    try:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        file_path = convert_to_jpg(filepath)
        make_imageresize(file_path)
        logging.info(f'{url} downloaded & saved as {file_path}')
    except IOError:
        pass


def download_txt(url, filepath):
    folder, _ = filepath.split('/')
    response = requests.get(url)
    response.raise_for_status()
    if 'text/plain' not in response.headers['Content-Type']:
        logging.info(f'{url} txt passed')
        return
    os.makedirs(folder, exist_ok=True)

    try:
        with open(filepath, 'w', encoding="utf-8") as f:
            f.write(response.content.decode("utf-8"))
            logging.info(f'{url} downloaded & saved as {filepath}')
    except IOError:
        pass


def fetch_hrefs(domain, category, start_page, end_page):
    if start_page >= end_page:
        end_page = start_page+1
    category_hrefs = []
    for page in range(start_page, end_page):
        page_category_link = f"{domain}/{category}/{page}"
        category_hrefs.extend(
            get_category_hrefs(make_soup(page_category_link), domain))
    return category_hrefs


def parse_book(href, domain):
    book_specification = {}
    soup = make_soup(href)
    title = get_book_title(soup)
    if not title:
        return

    filename = sanitize_filename(title)

    book_specification["title"] = title
    book_specification["author"] = get_book_author(soup)

    image_url = urljoin(domain, get_book_img_src(soup))
    img_filepath = os.path.join('images/', f'{filename}.jpg')

    download_img(image_url, img_filepath)
    book_specification["img_src"] = img_filepath

    txt_filepath = os.path.join('books/', f'{filename}.txt')
    txt_id = ''.join(char for char in href if char.isdigit())
    txt_url = urljoin(domain, f"txt.php?id={txt_id}")
    download_txt(txt_url, txt_filepath)
    book_specification["book_path"] = txt_filepath

    book_specification["comments"] = get_book_comments(soup)
    book_specification["genres"] = get_book_genres(soup)

    logging.info(f'process with {href=} - {title}')
    return book_specification


def parse_library():
    domain = r"http://tululu.org/"
    category = 'l55'
    args = get_args_parser().parse_args()
    start_page = args.start_page
    end_page = args.end_page
    hrefs = fetch_hrefs(domain, category, start_page, end_page)

    parsed_books = [parse_book(href, domain) for href in hrefs if href]
    info_books_file = "library.json"
    with open(info_books_file, "w") as file:
        json.dump(parsed_books, file, ensure_ascii=False, indent=4)
        logging.info(f'{info_books_file=} downloaded & saved!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parse_library()

