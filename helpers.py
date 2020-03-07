from bs4 import BeautifulSoup
from PIL import Image
import argparse
import lxml
import requests
import os
import logging
from resizeimage import resizeimage


def make_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


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


def make_imageresize(file_path, image_size, extension='.jpg'):
    _width, _height = image_size
    gorizontal = [_width, _height]
    vertical = [_height, _width]
    quadrate = [_width, _width]
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


def get_args_parser():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class)
    parser.add_argument('-start_page', '--start_page', type=int, default=1,
                        help='First lib page for parsing')
    parser.add_argument('-end_page', '--end_page', type=int, default=1,
                        help='Last lib page for parsing')
    parser.add_argument('-dest_folder', '--dest_folder',  type=str,
                        default="", help='download destination folder')
    parser.add_argument('-json_path', '--json_path',  type=str,
                        default="", help='final json results path')
    parser.add_argument('-skip_imgs', '--skip_imgs', action='store_true',
                        default=False, help='skip images download')
    parser.add_argument('-skip_txts', '--skip_txts', action='store_true',
                        default=False, help='skip txt files download')
    return parser