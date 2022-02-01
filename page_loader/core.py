import requests


def download(page_url, path):
    page = requests.get(page_url)
    return page
