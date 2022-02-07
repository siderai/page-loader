import os
import shutil
import logging
from urllib.parse import urlparse
from typing import List

import requests
from bs4 import BeautifulSoup


def download(url: str, content_path: str = '/home/downloads/') -> str:
    # save page as html
    name = parse_name(url, 'html')
    path = os.path.join(content_path, name)
    request = requests.get(url)
    with open(path, 'w+') as html:
        html.write(request.text)

    # prepare env to save page content (img, png, js, css)
    content_dir_name = parse_name(url, 'dir')
    path_for_files = os.path.join(content_path, content_dir_name)
    if not os.path.isdir(path_for_files):
        os.makedirs(path_for_files)

    soup = BeautifulSoup(request.content, 'html.parser')

    # save images from page
    img_items = soup.find_all('img')
    
    save_images(img_items, path_for_files, url)

    # save JS files 
    scripts = soup.find_all('script')
    save_scripts(scripts, path_for_files)

    # save CSS
    resources = soup.find_all('link')
    save_css(resources, path_for_files)

    # change url paths in html to local paths

    return path


def save_images(img_items: List[str], path_for_files: str, url: str):
    prefix = gen_images_prefix(url)
    for img in img_items:
        link = img.get('src')
        # download only from the same subdomain
        if is_equal_netloc(url, link): 
            print(link)
            if link.startswith('/'):
                link == urlparse(url).netloc + link
            if "http" in link:
                raw_img = requests.get(link, stream=True)
                img_name = prefix + parse_name(link, 'img')
                img_path = os.path.join(path_for_files, img_name)
                print(img_path)
                with open(img_path, "wb+") as f:
                    shutil.copyfileobj(raw_img.raw, f)


def gen_images_prefix(url: str):
    ''' 
    From 'https://ru.hexlet.io/projects/' get
    prefix like 'ru-hexlet-io'
    '''
    netloc = urlparse(url).netloc
    prefix = ''.join(
        char if char.isalnum() else '-' for char in netloc)
    return prefix


def is_equal_netloc(main_url, item_url):
    return urlparse(main_url).netloc == urlparse(item_url).netloc


def save_scripts(scripts: List[str], path_for_files: str):
    for script in scripts:
        if script.get('src'):
            link = script.get('src')
            if "http" in link:
                print(link)
                js = requests.get(link).text
                script_name = parse_name(link, 'js')
                script_path = os.path.join(path_for_files, script_name)
                with open(script_path, "w+") as f:
                    f.write(js)


def save_css(resources: List[str], path_for_files: str):
    for resource in resources:
        link = resource.get('href')
        if link.endswith('.css') and "http" in link:
            print(link)
            resource_content = requests.get(link).text
            resource_name = parse_name(link, 'resource')
            resource_path = os.path.join(path_for_files, resource_name)
            with open(resource_path, "w+") as f:
                f.write(resource_content)


# endings = {
#     'html': '.html',
#     'dir': '_files',
#     'script': '.js'
#     'css': '.css'
#     'jpg': '.jpg'
#     'png': '.png'
#     }

def parse_name(url: str, item_type: str):
    """ Parse URL to generate a name"""

    if '://' in url:
        link = url.split('://')[-1]
    else:
        link = url

    name = ''.join(
        char if char.isalnum() else '-' for char in link)
    if name[-1] == '-':
        name = name[:-2]

    # text files
    if item_type == 'script':
        if name.endswith('-js'):
            name = name.replace('-js', '.js')
    elif item_type == 'css':
        if name.endswith('-css'):
            name = name.replace('-css', '.css')
    # images
    elif item_type == 'img':
        if name.endswith('-jpg'):
            name = name.replace('-jpg', '.jpg')
        elif name.endswith('-png'):
            name = name.replace('-png', '.png')
    # html and dir for it's contents
    elif item_type == 'html':
        name += '.html'
    elif item_type == 'dir':
        name += '_files'

    return name














# сгенерировать имя папки с контентом
# создать папку с таким названием


# Итерация:
# спарсить имя изображения
# спарсить ссылку на изображение
# скачать изображение
# сгенерировать имя файла для локального хранения

# заменить в исходном Html





