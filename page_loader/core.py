import os
import logging

import requests
from bs4 import BeautifulSoup

from page_loader.services import parse_name, save_images, save_scripts, save_css


logging.basicConfig(level='DEBUG')
logger = logging.getLogger()


def download(url: str, content_path: str = '/home/downloads/') -> str:
    # save page as html
    name = parse_name(url, 'html')
    path = os.path.join(content_path, name)
    request = requests.get(url)
    if request.status_code != 200:
        logging.error('Initial request failed')
    with open(path, 'w+') as html:
        html.write(request.text)

    # prepare env to save page content (img, png, js, css)
    content_dir_name = parse_name(url, 'dir')
    path_for_files = os.path.join(content_path, content_dir_name)
    if not os.path.isdir(path_for_files):
        try:
            os.makedirs(path_for_files)
        except PermissionError('You have no rights to create '
                               'a directory with this path'):
            logging.error('Could not save to a local directory as '
                          'it does not exist and cannot be created')

    soup = BeautifulSoup(request.content, 'html.parser')

    # save images from page
    img_items = soup.find_all('img')
    save_images(img_items, path_for_files, url)

    # save JS files
    scripts = soup.find_all('script')
    save_scripts(scripts, path_for_files, url)

    # save CSS
    resources = soup.find_all('link')
    save_css(resources, path_for_files, url)

    # change url paths in html to local paths

    return path


# сгенерировать имя папки с контентом
# создать папку с таким названием


# Итерация:
# спарсить имя изображения
# спарсить ссылку на изображение
# скачать изображение
# сгенерировать имя файла для локального хранения

# заменить в исходном Html