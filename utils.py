from bs4 import BeautifulSoup
from PIL import Image
import lxml
import requests
import os
import logging
from resizeimage import resizeimage


def get_file_extension(url):
    return '.' + url.split('.')[-1]


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


def make_imageresize(file_path, extension='.jpg'):
    gorizontal = [285, 200]
    vertical = [200, 285]
    quadrate = [gorizontal[0], gorizontal[0]]
    if get_file_extension(file_path) == extension:

        fd_img = open(file_path, 'rb')
        img = Image.open(fd_img)

        try:
            if img.width > img.height:
                img = resizeimage.resize_contain(img, gorizontal)
            elif img.width == img.height:
                img = resizeimage.resize_contain(img, quadrate)
            else:
                img = resizeimage.resize_contain(img, vertical)
        except resizeimage.ImageSizeError:
            logging.info('ImageSizeError' + img)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(file_path, img.format)

        fd_img.close()
    else:
        pass


def make_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
