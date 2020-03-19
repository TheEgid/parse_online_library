import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler


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


def serve_start():
    env = Environment(loader=FileSystemLoader('templates'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')

    dest_folder = 'pages'
    if dest_folder:
        os.makedirs(dest_folder, exist_ok=True)

    books_chunks = get_books_chunks()
    for count, books_chunk in enumerate(books_chunks, start=1):
        rendered_page = template.render(books=books_chunk,
                                        pages_amount=len(books_chunks),
                                        this_page=count)

        with open(f'{dest_folder}/index{count}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    global server
    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def serve_stop():
    try:
        server.socket.close()
        server.shutdown()
    except NameError:
        pass


if __name__ == '__main__':
    serve_start()
