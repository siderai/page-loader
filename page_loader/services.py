import logging
import os
import shutil
from urllib.parse import urljoin, urlparse

import requests

logging.basicConfig(level='DEBUG')
logger = logging.getLogger()

# functions for page_loader.py


def save_image(img: str, path_for_files: str, url: str) -> str:
    ''' Save images for offline access to page,
        then return img's local path'''
    # parse image url
    link = img['src']
    if not link:
        logger.debug(f'Empty link in img src: {img}')
        link = img['href']
        if not link:
            logger.debug(f'Empty link in img href: {img}')
            return ''
    # equalize relative and absolute url path
    link = unificate_url(url, link)
    logger.debug(f'Resource full link parsed: {link}')
    if is_equal_hostname(url, link):
        raw_img = requests.get(link, stream=True)
        img_name = parse_name(link, 'img')
        img_path = os.path.join(path_for_files, img_name)
        with open(img_path, "wb+") as f:
            shutil.copyfileobj(raw_img.raw, f)
        logger.debug(f'Img saved: {img_path}')
        return img_path


def save_script(script: str, path_for_files: str, url: str) -> str:
    ''' Parse link to local script, download
        the file and return its local path '''
    link = script.get('src')
    if not link:
        logger.debug(f'Empty link in script src: {script}')
        link = script.get('href')
        if not link:
            logger.debug(f'Empty link in script href: {script}')
            return ''
    link = unificate_url(url, link)
    logger.debug(f'Script full link parsed: {link}')
    if is_equal_hostname(url, link):
        js_response = requests.get(link)
        js_response.encoding == 'utf-8'
        script_name = parse_name(link, 'js')
        script_path = os.path.join(path_for_files, script_name)
        with open(script_path, "w+") as f:
            f.write(js_response.text)
        logger.debug(f'Script saved: {script_path}')
        return script_path


def save_resource(resource: str, path_for_files: str, url: str) -> str:
    ''' Parse link to css file, download the file and return its local path '''
    # parse target url
    link = resource.get('href')
    if not link:
        logger.debug(f'Empty link in resource href: {resource}')
        link = resource.get('src')
        if not link:
            logger.debug(f'Empty link in resource src: {resource}')
    link = unificate_url(url, link)
    logger.debug(f'Resource full link parsed: {link}')
    if is_equal_hostname(url, link):
        res = requests.get(link)
        res.encoding = 'utf-8'
        if link.endswith('.css'):
            item_type = 'css'
        else:
            item_type = 'html'
        resource_name = parse_name(link, f'{item_type}')
        resource_path = os.path.join(path_for_files, resource_name)
        if item_type == 'css':
            with open(resource_path, "w+") as f:
                f.write(res.text)
            logger.debug(f'Resource saved: {resource_path}')
        else:
            with open(resource_path, "w+") as f:
                f.write(res.text)
        return resource_path


def parse_name(url: str, item_type: str):
    """ Parse URL to generate a name"""

    link = delete_scheme_from_url(url)
    name = format_url_to_name(link)
    name = switch_extension(name, item_type)

    return name

# Below there are useful internal functions


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


def switch_extension(name: str, item_type: str) -> str:
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
        logger.debug(f'Failed to format name extension: {name}')

    return name


def unificate_url(url: str, link: str) -> str:
    ''' Equalize relative and absolute paths '''
    if link.startswith('/'):
        link = urljoin(url, link)
    return link


def is_equal_hostname(main_url: str, item_url: str):
    '''Check if asset has the same host as the downloaded page.'''
    return urlparse(main_url).hostname == urlparse(item_url).hostname
