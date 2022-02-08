import os
import shutil
import logging
from urllib.parse import urlparse
from typing import List

import requests


def save_images(img_items: List[str], path_for_files: str, url: str):
    ''' Save images to enable full offline access to page '''
    prefix = gen_images_prefix(url)
    for img in img_items:
        link = img.get('src')
        if not link:
            logging.debug(f'Empty link in image object: {img}')
        # download only from the same subdomain
        if is_equal_netloc(url, link):
            print(link)
            # unificate url
            if link.startswith('/'):
                link == urlparse(url).netloc + link
            raw_img = requests.get(link, stream=True)
            if raw_img.status_code != 200:
                logging.warning('Could not connect to server, '
                                f'image url: {link}')
            img_name = prefix + parse_name(link, 'img')
            img_path = os.path.join(path_for_files, img_name)
            try:
                with open(img_path, "wb+") as f:
                    shutil.copyfileobj(raw_img.raw, f)
            except PermissionError():
                logging.warning('Could not save img to file '
                                'due to permission error')


def gen_images_prefix(url: str) -> str:
    ''' From 'https://ru.hexlet.io/projects/' get name prefix
        like 'ru-hexlet-io' '''
    netloc = urlparse(url).netloc
    prefix = ''.join(
        char if char.isalnum() else '-' for char in netloc)
    return prefix


def is_equal_netloc(main_url, item_url):
    return urlparse(main_url).netloc == urlparse(item_url).netloc


def save_scripts(scripts: List[str], path_for_files: str, url):
    for script in scripts:
        link = script.get('src')
        if is_equal_netloc(url, link):
            print(link)
            js_response = requests.get(link)
            if js_response.status_code != 200:
                logging.warning(f'Could not download script from src: {link}')
            script_content = js_response.text
            script_name = parse_name(link, 'js')
            script_path = os.path.join(path_for_files, script_name)
            with open(script_path, "w+") as f:
                f.write(script_content)


def save_css(resources: List[str], path_for_files: str, url: str):
    for resource in resources:
        link = resource.get('href')
        if is_equal_netloc(url, link) and link.endswith('.css'):
            print(link)
            if link.startswith('/'):
                link == urlparse(url).netloc + link
            resource = requests.get(link)
            if resource.status_code != 200:
                logging.warning('Could not download '
                                f'resource from href: {link}')
            resource_content = resource.text
            resource_name = parse_name(link, 'resource')
            resource_path = os.path.join(path_for_files, resource_name)
            with open(resource_path, "w+") as f:
                f.write(resource_content)


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
    if item_type == 'script':
        if name.endswith('-js'):
            name = name[:-3] + '.js'
    elif item_type == 'css':
        if name.endswith('-css'):
            name = name[:-4] + '.css'
    # images
    elif item_type == 'img':
        if name.endswith('-jpg'):
            name = name[:-4] + '.jpg'
        elif name.endswith('-png'):
            name = name[:-4] + '.png'
    # html and dir for it's contents
    elif item_type == 'html':
        name += '.html'
    elif item_type == 'dir':
        name += '_files'
    else:
        logging.debug(f'Failed to switch name ending: {name}')
    return name
