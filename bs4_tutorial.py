import requests
from bs4 import BeautifulSoup
import lxml


def make_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_title_text(soup):
    title_tag = soup.find('main').find('header').find('h1')
    return title_tag.text


def get_post_image(soup):
    return soup.find('img', class_='attachment-post-image')['src']


def get_entry_content(soup, end_of_content):
    elements = []
    tags = soup.findAll({'entry_content': True, 'h3': True, 'p': True, })

    for element in tags:
        if not element.find('a'):
            elements.append(element.text)

    elements = [el.replace('\n', ' ') for el in elements]
    end = elements.index(end_of_content)
    return ' '.join(elements[:end])


if __name__ == '__main__':
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    soup = make_soup(url)

    print(get_title_text(soup))
    print(get_post_image(soup))
    print(
        get_entry_content(soup, end_of_content='Do You Count Your Blessings?'))
