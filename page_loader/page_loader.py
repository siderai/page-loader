import argparse
import os

import requests


def get_name(page_url: str):
    if '://' in page_url:
        link = page_url.split('://')[1]
    else:
        link = page_url
    # get output file name via formatting url
    name = ''
    for i, char in enumerate(link):
        if char.isalnum():
            name += char
        elif i == len(link) - 1:
            break
        else:
            name += '-'
    name += '.html'
    return name


def download(page_url: str, folder: str = '/home/downloads/') -> str:
    name = get_name(page_url)
    path = os.path.join(folder, name)
    with open(path, 'w') as html:
        page = requests.get(page_url)
        html.write(page.text)
    return path


def main():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('link', type=str)
    parser.add_argument('-o', '--output', default='/home/downloads/',
                        help='set output folder')
    args = parser.parse_args()
    print(download(args.link, output=args.output))


if __name__ == '__main__':
    main()
