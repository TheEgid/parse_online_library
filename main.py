import requests
import os
import logging
from pathvalidate import sanitize_filename

from utils import get_path, convert_to_jpg, make_soup, make_imageresize


# def get_book_info(soup):
#     elements = list()
#     try:
#         tags = soup.find_all({'entry_content': True, 'h1': True, })
#         [elements.append(element.text) for element in tags]
#         elements = [el.replace('\xa0', ' ') for el in elements][0]
#         _elements = ''.join(elements)
#         book_title, book_author = _elements.split('::')
#         return {'book_title': book_title.strip(),
#                 'book_author': book_author.strip()}
#     except ValueError:
#         return


def get_book_title(soup):
    elements = list()
    try:
        tags = soup.find_all({'entry_content': True, 'h1': True, })
        [elements.append(element.text) for element in tags]
        elements = [el.replace('\xa0', ' ') for el in elements][0]
        _elements = ''.join(elements)
        book_title, _ = _elements.split('::')
        return book_title.strip().replace('. ', '_').replace(': ', '_')
    except ValueError:
        return


def get_book_image(soup):
    try:
        div = soup.find('div', class_='bookimage')
        return div.find('img')['src']
    except ValueError:
        return


def download_img(url, filename, folder='images/'):
    filename = f'{filename}.jpg'
    sanitize_filename(filename)
    response = requests.get(url)
    response.raise_for_status()
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
    if "<!DOCTYPE html" in str(response.content):
        logging.info(f'{url} is HTML: passed')
        return
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as f:
        f.write(response.content)
        logging.info(f'{url} downloaded & saved as {filepath}')


def main():
    logging.basicConfig(level=logging.INFO)
    start_page = 0
    end_page = 11

    for id in range(start_page, end_page):
        info_link = f"http://tululu.org/b{id}/"
        txt_link = f"http://tululu.org/txt.php?id={id}/"
        soup = make_soup(info_link)

        book_title = get_book_title(soup)

        if book_title:
            download_txt(txt_link, book_title)
            book_img = get_book_image(soup)
            download_img(f'http://tululu.org/{book_img}', book_title)


if __name__ == '__main__':
    main()

