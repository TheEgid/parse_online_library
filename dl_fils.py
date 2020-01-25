import requests
import os
import logging
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from PIL import Image


def get_path(file):
    module_dir = os.path.dirname(__file__)
    return os.path.join(module_dir, file)


def convert_to_jpg(file):
    file = get_path(file)
    file_name, file_extension = os.path.splitext(file)
    if file_extension.lower() != 'jpg':
        logging.info(f' Process with {file_name}{file_extension}')
        im = Image.open(file)
        rgb_im = im.convert('RGB')
        file = f'{file_name}.jpg'
        rgb_im.save(file)
    return file


def make_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_book_info(soup):
    elements = list()
    try:
        tags = soup.findAll({'entry_content': True, 'h1': True, })
        [elements.append(element.text) for element in tags]
        elements = [el.replace('\xa0', ' ') for el in elements][0]
        _elements = ''.join(elements)
        book_title, book_author = _elements.split('::')
        return {'book_title': book_title.strip(),
                'book_author': book_author.strip()}
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
        file_path = convert_to_jpg(filename)
        logging.info(f'{url} downloaded & saved as {file_path}')
    except IOError as err:
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

    for id in range(start_page, end_page, 1):
        info_link = f"http://tululu.org/b{id}/"
        txt_link = f"http://tululu.org/txt.php?id={id}/"
        root_link = f"http://tululu.org/"
        soup = make_soup(info_link)
        book_info = get_book_info(soup)
        if book_info:
            book_title = book_info['book_title']
            book_title = book_title.replace('. ', '_').replace(': ', '_')
            download_txt(url=txt_link, filename=book_title)
            book_img = get_book_image(soup)
            img_link = f'{root_link}{book_img}'
            download_img(url=img_link, filename=book_title)


if __name__ == '__main__':
    main()

