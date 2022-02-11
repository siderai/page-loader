import os
import shutil
import logging
from urllib.parse import urlparse, urljoin

import requests


def save_image(img: str, path_for_files: str, url: str) -> str:
    ''' Save images to enable full offline access to page,
        then return img's path to be updated in resuling html '''
    # parse image url
    link = img['src']
    if not link:
        logging.debug(f'Empty link in img src: {img}')
        link = img['href']
        if not link:
            logging.error(f'Empty link in img href: {img}')
            return
    # equalize relative and absolute url path
    link = unificate_url(url, link)
    logging.debug(f'Resource full link parsed: {link}')
    if is_equal_hostname(url, link):
        raw_img = requests.get(link, stream=True)
        if raw_img.status_code == 404:
            logging.error('Could not connect to server, '
                          f'image url: {link}')
        img_name = parse_name(link, 'img')
        img_path = os.path.join(path_for_files, img_name)
        with open(img_path, "wb+") as f:
            shutil.copyfileobj(raw_img.raw, f)
        logging.debug(f'Img saved: {img_path}')
    return img_path


def save_script(script: str, path_for_files: str, url) -> str:
    ''' Parse link to local script, download
        the file and return its local path '''
    link = script.get('src')
    if not link:
        logging.debug(f'Empty link in script src: {script}')
        link = script.get('href')
        if not link:
            logging.error(f'Empty link in script href: {script}')
            return
    link = unificate_url(url, link)
    logging.debug(f'Script full link parsed: {link}')
    if is_equal_hostname(url, link):
        js_response = requests.get(link)
        if js_response.status_code == 404:
            logging.error(f'Could not download script from src: {link}')
        script_content = js_response.text
        script_name = parse_name(link, 'js')
        script_path = os.path.join(path_for_files, script_name)
        with open(script_path, "w+") as f:
            f.write(script_content)
            logging.debug(f'Script saved: {script_path}')
        return script_path


def save_resource(resource: str, path_for_files: str, url: str) -> str:
    ''' Parse link to css file, download the file and return its local path '''
    # parse target url
    link = resource.get('href')
    if not link:
        logging.debug(f'Empty link in resource href: {resource}')
        link = resource.get('src')
        if not link:
            logging.error(f'Empty link in resource src: {resource}')
    link = unificate_url(url, link)
    logging.debug(f'Resource full link parsed: {link}')
    if is_equal_hostname(url, link):
        res = requests.get(link)
        if resource.status_code == 404:
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
        return resource_path


def unificate_url(url: str, link: str) -> str:
    ''' Equalize relative and absolute paths '''
    if link.startswith('/'):
        link = urljoin(url, link)
    return link


def is_equal_hostname(main_url, item_url):
    ''' download only from the same subdomain'''
    return urlparse(main_url).hostname == urlparse(item_url).hostname


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
