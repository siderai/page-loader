import os
import shutil
import logging
from urllib.parse import urlparse, urljoin
from typing import List

import requests


def save_images(img_items: List[str], path_for_files: str, url: str):
    ''' Save images to enable full offline access to page '''
    prefix = gen_images_prefix(url)
    for img in img_items:
        # parse image url
        link = img.get('src')
        if not link:
            logging.debug(f'Empty link in img src: {img}')
            link = img.get('href')
            if not link:
                logging.error(f'Empty link in img href: {img}')
                continue
        # unificate url
        if link.startswith('/'):
            link = urljoin(url, link)
            logging.debug(f'Img link parsed: {link}')
        logging.debug(f'Resource full link parsed: {link}')
        # download only from the same subdomain
        if is_equal_hostname(url, link):
            raw_img = requests.get(link, stream=True)
            if raw_img.status_code != 200:
                logging.error('Could not connect to server, '
                                f'image url: {link}')
            img_name = prefix + parse_name(link, 'img')
            img_path = os.path.join(path_for_files, img_name)
            try:
                with open(img_path, "wb+") as f:
                    shutil.copyfileobj(raw_img.raw, f)
                logging.debug(f'Img saved: {img_path}')
            except PermissionError():
                logging.error('Could not save img to file '
                                'due to permission error')


def gen_images_prefix(url: str) -> str:
    ''' From 'https://ru.hexlet.io/projects/' get name prefix
        like 'ru-hexlet-io' '''
    hostname = urlparse(url).hostname
    prefix = ''.join(
        char if char.isalnum() else '-' for char in hostname)
    return prefix


def is_equal_hostname(main_url, item_url):
    return urlparse(main_url).hostname == urlparse(item_url).hostname


def save_scripts(scripts: List[str], path_for_files: str, url):
    for script in scripts:

        link = script.get('src')
        if not link:
            logging.debug(f'Empty link in script src: {script}')
            link = script.get('href')
            if not link:
                logging.error(f'Empty link in script href: {script}')
                continue
        if link.startswith('/'):
            link = urljoin(url, link)
            logging.debug(f'Script link parsed: {link}')
        logging.debug(f'Resource full link parsed: {link}')
        if is_equal_hostname(url, link):
            js_response = requests.get(link)
            if js_response.status_code != 200:
                logging.error(f'Could not download script from src: {link}')
            script_content = js_response.text
            script_name = parse_name(link, 'js')
            script_path = os.path.join(path_for_files, script_name)
            with open(script_path, "w+") as f:
                f.write(script_content)
                logging.debug(f'Script saved: {script_path}')


def save_local_resources(resources: List[str], path_for_files: str, url: str):
    for resource in resources:
        # parse target url
        link = resource.get('href')
        if not link:
            logging.debug(f'Empty link in resource href: {resource}')
            link = resource.get('src')
            if not link:
                logging.error(f'Empty link in resource src: {resource}')
        # equalize relative and absolute url path
        if link.startswith('/'):
            link = urljoin(url, link)
            logging.debug(f'Resource link parsed: {link}')
        logging.debug(f'Resource full link parsed: {link}')
        if is_equal_hostname(url, link):
            res = requests.get(link)
            if resource.status_code != 200:
                logging.error('Could not download '
                                f'resource from href: {link}')
            resource_content = res.text
            if link.endswith('.css'):
                item_type = 'css'
            else:
                item_type = 'html'
            resource_name = parse_name(link, f'{item_type}')
            resource_path = os.path.join(path_for_files, resource_name)
            with open(resource_path, "w+") as f:
                f.write(resource_content)
                logging.debug(f'Resource saved: {resource_path}')


def parse_name(url: str, item_type: str):
    """ Parse URL to generate a name"""

    link = delete_scheme_from_url(url)
    name = format_url_to_name(link)
    name = switch_ending(name, item_type)

    return name


def delete_scheme_from_url(url: str) -> str:
    if '://' in url:
        link = url.split('://')[-1]
    else:
        link = url
    return link


def format_url_to_name(link: str) -> str:
    name = ''.join(
        char if char.isalnum() else '-' for char in link)
    if name[-1] == '-':
        name = name[:-1]
    return name


def switch_ending(name: str, item_type: str) -> str:
    ''' Edit ending of parsed name according to format '''
    # text files
    if name.endswith('-js'):
        name = name[:-3] + '.js'
    elif name.endswith('-css'):
        name = name[:-4] + '.css'
    # images
    elif name.endswith('-jpg'):
        name = name[:-4] + '.jpg'
    elif name.endswith('-png'):
        name = name[:-4] + '.png'
    # html and dir for it's contents
    elif item_type == 'html':
        name += '.html'
    elif item_type == 'dir':
        name += '_files'
    else:
        logging.debug(f'Failed to format name ending: {name}')

    return name
