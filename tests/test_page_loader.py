from tempfile import TemporaryDirectory, TemporaryFile
from page_loader import download, get_name

import pytest


@pytest.fixture
def url():
    return 'https://python-poetry.org/docs/'


@pytest.fixture
def urla():
    return 'en.wikipedia.org/wiki/URL'


@pytest.fixture
def hexlet():
    return 'https://ru.hexlet.io/courses'


@pytest.fixture
def default():
    return '/home/downloads'


@pytest.fixture
def hexletsaved():
    with open('tests/fixtures/courses.html') as courses:
        page = courses.read()
    return page


def test_get_name(url, urla, default):
    assert get_name(url) == 'python-poetry-org-docs.html'
    assert get_name(urla) == 'en-wikipedia-org-wiki-URL.html'


# def test_download(hexletsaved, hexlet, folder='/'):
#     file_name = get_name(hexlet)
#     with TemporaryDirectory(folder) as td:
#         path = download(hexlet, td)
#         # path is correct
#         assert path == f'{td}{file_name}'
#         with open(path) as html:
#             page = html.read()
#             assert page == hexletsaved
