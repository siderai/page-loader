import os
import logging

import requests
from bs4 import BeautifulSoup

from page_loader.services import *


logging.basicConfig(level='DEBUG')
logger = logging.getLogger()


def download(url: str, content_path: str) -> str:
    # make initial request
    request = requests.get(url)
    if request.status_code != 200:
        logging.error('Initial request failed '
                      f'with code: {request.status_code}')
        raise Exception('Initial connection failed!')
    else:
        logging.debug(f'Connection established: {url}')
    name = parse_name(url, 'html')
    path = os.path.join(content_path, name)
    with open(path, 'w+') as html:
        html.write(request.text)

    # prepare file system for saving page content (img, png, js, css)
    content_dir_name = parse_name(url, 'dir')
    path_for_files = os.path.join(content_path, content_dir_name)
    if not os.path.isdir(path_for_files):
        try:
            os.makedirs(path_for_files)
            logging.debug(f'Created assets directory: {path_for_files}')
        except PermissionError('You have no rights to create '
                               'a directory with this path'):
            logging.error('Could not save to a local directory as '
                          'it does not exist and cannot be created')

    soup = BeautifulSoup(request.content, 'html.parser')

    # save image from page, then replace its url by path of downloaded file
    img_items = soup.find_all('img')
    for img in img_items:
        local_path_to_img = save_image(img, path_for_files, url)
        if local_path_to_img:
            relpath = os.path.relpath(local_path_to_img, content_dir_name)
            img['src'] = relpath

    # save JS files
    scripts = soup.find_all('script')
    for script in scripts:
        local_path_to_script = save_script(script, path_for_files, url)
        if local_path_to_script:
            relpath = os.path.relpath(local_path_to_script, content_dir_name)
            script['src'] = relpath

    # save CSS
    resources = soup.find_all('link')
    for res in resources:
        local_path_to_res = save_resource(res, path_for_files, url)
        if local_path_to_res:
            relpath = os.path.relpath(local_path_to_res, content_dir_name)
            res['href'] = relpath

    # save page as html locally

    with open(path, 'w+') as html:
        html.write(soup.prettify())

    return path
