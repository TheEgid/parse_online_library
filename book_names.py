# import requests
# from bs4 import BeautifulSoup
# import lxml
#
#
# def make_soup(url):
#     response = requests.get(url)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, 'lxml')
#     return soup
#
#
# def get_title_text(soup):
#     title_tag = soup.find('main').find('header').find('h1')
#     return title_tag.text
#
#
# def get_post_image(soup):
#     div = soup.find('div', class_='bookimage')
#     return div.find('img')['src']
#
#
# def get_entry_content(soup, end_of_content):
#     elements = []
#     tags = soup.findAll({'entry_content': True, 'h3': True, 'p': True, })
#
#     for element in tags:
#         if not element.find('a'):
#             elements.append(element.text)
#
#     elements = [el.replace('\n', ' ') for el in elements]
#     end = elements.index(end_of_content)
#     return ' '.join(elements[:end])
#
#
# def get_book_name(soup):
#     elements = list()
#     tags = soup.findAll({'entry_content': True, 'h1': True, })
#     [elements.append(element.text) for element in tags]
#     elements = [el.replace('\xa0', ' ') for el in elements][0]
#     _elements = ''.join(elements)
#     book_title, book_author = _elements.split('::')
#     return {'book_title': book_title.strip(), 'book_author': book_author.strip()}
#
#
# if __name__ == '__main__':
#     url = 'http://tululu.org/b9/'
#     soup = make_soup(url)
#     print(get_post_image(soup))
#     # print(get_title_text(soup))
#     # print(get_post_image(soup))
#     # print(
#     #     get_entry_content(soup, end_of_content='Do You Count Your Blessings?'))
