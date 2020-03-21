import json
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape


def chunks(_list, chunk_size):
    """Yield successive chunk-sized chunks from list.
    https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """
    for i in range(0, len(_list), chunk_size):
        yield _list[i:i + chunk_size]


def get_books_chunks(amount_on_page=10):
    with open('library.json') as json_file:
        books = json.load(json_file)
    return list(chunks(books, amount_on_page))


def create_pages(pages_folder='pages'):
    env = Environment(loader=FileSystemLoader('templates'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    books_chunks = get_books_chunks()
    for count, books_chunk in enumerate(books_chunks, start=1):
        rendered_page = template.render(books=books_chunk,
                                        pages_amount=len(books_chunks),
                                        this_page=count)
        rendered_page_filepath = f'{pages_folder}/index{count}.html'
        with open(rendered_page_filepath, 'w', encoding="utf8") as file:
            logging.info(f'Create Page: {rendered_page_filepath}')
            file.write(rendered_page)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    create_pages()
