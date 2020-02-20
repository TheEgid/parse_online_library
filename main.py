import requests
import os
import logging
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from utils import get_path, convert_to_jpg, make_soup, make_imageresize
from parse_tululu_category import fetch_hrefs


def get_book_title(soup):
    try:
        h1 = soup.select_one('#content > h1').text
        book_title, _ = h1.split('::')
        return book_title.strip().replace('. ', '_').replace(': ', '_')
    except (ValueError, AttributeError):
        return


def get_book_author(soup):
    try:
        h1 = soup.select_one('#content > h1').text
        _, book_author = h1.split('::')
        return book_author.strip()
    except (ValueError, AttributeError):
        return
    
def get_book_image(soup):
    try:
        return soup.select_one('.bookimage > a > img').get('src')
    except (ValueError, AttributeError):
        return


def get_book_comments(soup):
    comments = []
    try:
        raw_comments = soup.select('#content > div.texts')
        for raw_comment in raw_comments:
           comment = raw_comment.select_one("span.black").text.strip()
           comments.append(comment)
        return comments
    except (ValueError, AttributeError):
        return


def get_book_genres(soup):
    genres = []
    try:
        [genres.append(genre.text) for genre in soup.select('span.d_book > a')]
        return genres
    except (TypeError, AttributeError):
        return


def download_img(url, filename, folder='images/'):
    filename = f'{filename}.jpg'
    sanitize_filename(filename)
    response = requests.get(url)
    response.raise_for_status()
    if 'image' not in response.headers['Content-Type']:
        logging.info(f'{url} image passed')
        return
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    try:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        file_path = convert_to_jpg(filepath)
        make_imageresize(file_path)
        logging.info(f'{url} downloaded & saved as {file_path}')
    except IOError:
        pass


def download_txt(url, filename, folder='books/'):
    filename = f'{filename}.txt'
    sanitize_filename(filename)
    response = requests.get(url)
    response.raise_for_status()
    if 'text/plain' not in response.headers['Content-Type']:
        logging.info(f'{url} txt passed')
        return
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding="utf-8") as f:
        f.write(response.content.decode("utf-8"))
        logging.info(f'{url} downloaded & saved as {filepath}')


def main():
    logging.basicConfig(level=logging.INFO)
    domain = r"http://tululu.org/"
    category = 'l55'
    category_hrefs = fetch_hrefs(domain, category, amount=100)

    for href in category_hrefs:
        soup = make_soup(href)
        book_author = get_book_author(soup)
        print(book_author)
        book_title = get_book_title(soup)
        print(book_title)

        if book_title:
            txt_id = ''.join(
                char for char in 'http://tululu.org/b550/' if char.isdigit())
            txt_link = urljoin(domain, f"txt.php?id={txt_id}")
            #download_txt(txt_link, book_title)
            print(txt_link)
            book_img = get_book_image(soup)
            print(book_img)
            #download_img(urljoin(domain, book_img), book_title)
            book_comments = get_book_comments(soup)
            print(book_comments)
            book_genres = get_book_genres(soup)
            print(book_genres)


if __name__ == '__main__':
    main()

