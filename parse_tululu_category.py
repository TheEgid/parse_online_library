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


def download_file(url, filepath, image_size=None):
    try:
        folder, _ = os.path.split(filepath)
        os.makedirs(folder, exist_ok=True)
        response = requests.get(url)
        response.raise_for_status()
        content_type = response.headers['Content-Type']

        if 'image' in content_type:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            file_path = convert_to_jpg(filepath)
            make_imageresize(file_path, image_size)
        elif 'text/plain' in content_type:
            with open(filepath, 'w', encoding="utf-8") as f:
                f.write(response.content.decode("utf-8"))
        else:
            raise ValueError

        logging.info(f'{url} downloaded & saved as {filepath} ({content_type})')

    except (requests.exceptions.HTTPError, ValueError):
        logging.info(f'{url} passed')
        pass

    except (IOError, UnicodeDecodeError):
        logging.info(f'{url} file system error: passed')
        pass


def fetch_hrefs(domain, category, start_page, end_page):
    if start_page >= end_page + 1:
        start_page = end_page + 1
    category_hrefs = []
    for page in range(start_page, end_page + 1):
        page_category_link = f'{domain}/{category}/{page}'
        category_hrefs.extend(
            get_category_hrefs(make_soup(page_category_link), domain))
    return category_hrefs


def parse_book(href, dest_folder, image_size, skip_txts, skip_imgs):

    if dest_folder:
        os.makedirs(dest_folder, exist_ok=True)
    book_specification = {}
    soup = make_soup(href)
    title = get_book_title(soup)
    if not title:
        return

    book_specification["title"] = title
    book_specification["author"] = get_book_author(soup)

    filename = sanitize_filename(title)

    if not skip_txts:
        txt_filepath = os.path.join(dest_folder, 'books', f'{filename}.txt')
        txt_id = ''.join(char for char in href if char.isdigit())
        txt_url = urljoin(href, f'/txt.php?id={txt_id}')
        download_file(txt_url, txt_filepath)
        book_specification["book_path"] = txt_filepath

    if not skip_imgs:
        image_url = urljoin(href, get_book_img_src(soup))
        img_filepath = os.path.join(dest_folder, 'images', f'{filename}.jpg')
        download_file(image_url, img_filepath, image_size)
        book_specification["img_src"] = img_filepath

    book_specification["comments"] = get_book_comments(soup)
    book_specification["genres"] = get_book_genres(soup)

    logging.info(f'process with {href=} - {title}')
    return book_specification


def parse_library():
    logging.basicConfig(level=logging.INFO)
    domain = 'http://tululu.org'
    json_file = 'library.json'
    category = r'l55'
    image_size = [285, 200]
    args = get_args_parser().parse_args()

    hrefs = fetch_hrefs(domain, category, args.start_page, args.end_page)
    parsed_books = [parse_book(href, args.dest_folder,
                               image_size, args.skip_txts, args.skip_imgs)
                    for href in hrefs if href]

    json_books_file = os.path.join(args.dest_folder, json_file)
    if args.json_path:
        os.makedirs(args.json_path, exist_ok=True)
        json_books_file = os.path.join(args.json_path, json_file)

    with open(json_books_file, "w") as f:
        json.dump(parsed_books, f, ensure_ascii=False, indent=4)
        logging.info(f'{json_books_file=} book specifications downloaded & saved!')


if __name__ == '__main__':
    parse_library()

