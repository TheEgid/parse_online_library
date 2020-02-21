from urllib.parse import urljoin


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


def get_book_img_src(soup):
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
    try:
        return [genre.text for genre in soup.select('span.d_book > a')]
    except (TypeError, AttributeError):
        return


def get_book_category_href(href_block, domain):
    try:
        href = href_block.select_one('a').get('href')
        book_href = urljoin(domain, href)
        return book_href
    except (TypeError, AttributeError):
        return


def get_category_hrefs(soup, domain):
    category_hrefs = []
    try:
        href_blocks = soup.select('table.d_book')
        for href_block in href_blocks:
            category_hrefs.append(get_book_category_href(href_block, domain))
        return category_hrefs
    except (TypeError, AttributeError):
        return

