import json
import logging
import configparser
import argparse
import os
import more_itertools
from functools import lru_cache
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pathlib


@lru_cache(maxsize=128)
def is_book_exists(book_txt):
    settings = load_settings()
    url = settings['url_schema_settings']['BOOK_URL']
    folder = ''.join(char for char in url if char.isalpha())
    fullpath = os.path.join(folder, book_txt)
    return pathlib.Path(fullpath).exists()


def get_books_from_file(library_filepath):
    with open(library_filepath, encoding='utf8') as json_file:
        books = json.load(json_file)
    return [book for book in books if is_book_exists(book['book_txt'])]


def save_rendered_page(rendered_page_filepath, rendered_page):
    with open(rendered_page_filepath, 'w', encoding="utf8") as file:
        logging.info(f'Create Page: {rendered_page_filepath}')
        file.write(rendered_page)


def get_template(template_folder, template_file):
    env = Environment(loader=FileSystemLoader(template_folder),
                      autoescape=select_autoescape(['html', 'xml']))
    settings = load_settings()
    env.globals['STATIC_URL'] = settings['url_schema_settings']['STATIC_URL']
    env.globals['BOOK_IMG_URL'] = settings['url_schema_settings']['BOOK_IMG_URL']
    env.globals['BOOK_URL'] = settings['url_schema_settings']['BOOK_URL']
    return env.get_template(template_file)


def create_pages(template_folder, template_file, library_filepath,
                 pages_folder, amount_on_page):
    books = get_books_from_file(library_filepath)
    books_chunks = list(more_itertools.chunked(books, amount_on_page))
    template = get_template(template_folder, template_file)
    for count, books_chunk in enumerate(books_chunks, start=1):
        rendered_page = template.render(books=books_chunk,
                                        pages_amount=len(books_chunks),
                                        this_page=count)
        page_name = f'index{count}.html'
        rendered_page_filepath = os.path.join(pages_folder, page_name)
        save_rendered_page(rendered_page_filepath, rendered_page)


def load_settings():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config


def get_args_parser():
    settings = load_settings()
    parser = argparse.ArgumentParser()
    parser.add_argument('-template_folder', '--template_folder', type=str,
                        default=settings["main_settings"]["TEMPLATE_FOLDER"])
    parser.add_argument('-template_file', '--template_file', type=str,
                        default=settings["main_settings"]["TEMPLATE_FILE"])
    parser.add_argument('-library_filepath', '--library_filepath', type=str,
                        default=settings["main_settings"]["LIBRARY_FILEPATH"])
    parser.add_argument('-pages_folder', '--pages_folder', type=str,
                        default=settings["main_settings"]["PAGES_FOLDER"])
    parser.add_argument('-amount_on_page', '--amount_on_page', type=int,
                        default=settings["main_settings"]["AMOUNT_ON_PAGE"])
    return parser


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = get_args_parser().parse_args()
    create_pages(template_folder=args.template_folder,
                 template_file=args.template_file,
                 library_filepath=args.library_filepath,
                 pages_folder=args.pages_folder,
                 amount_on_page=args.amount_on_page)
