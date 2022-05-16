from urllib.parse import urljoin

import pytest
from page_loader.services import (delete_scheme_from_url, format_url_to_name,
                                  is_equal_hostname, parse_name,
                                  switch_extension, unificate_url)


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
    with open('tests/fixtures/courses_updated.html') as courses:
        page = courses.read()
    return page


def test_delete_scheme_from_url(hexlet):
    assert delete_scheme_from_url(hexlet) == 'ru.hexlet.io/courses'
    no_scheme_url = 'www.ru.hexlet.io/courses'
    assert delete_scheme_from_url(no_scheme_url) == no_scheme_url


def test_format_url_to_name():
    assert format_url_to_name('ru.hexlet.io/courses') == 'ru-hexlet-io-courses'


def test_switch_extension():
    assert switch_extension('ru-hexlet-io-courses-js',
                            'script') == 'ru-hexlet-io-courses.js'
    assert switch_extension('ru-hexlet-io-courses-css',
                            'css') == 'ru-hexlet-io-courses.css'
    assert switch_extension('ru-hexlet-io-courses-jpg',
                            'img') == 'ru-hexlet-io-courses.jpg'
    assert switch_extension('ru-hexlet-io-courses-png',
                            'img') == 'ru-hexlet-io-courses.png'
    assert switch_extension('ru-hexlet-io-courses',
                            'html') == 'ru-hexlet-io-courses.html'
    assert switch_extension('ru-hexlet-io-courses',
                            'dir') == 'ru-hexlet-io-courses_files'
    assert switch_extension('ru-hexlet-io-courses',
                            'smth') == 'ru-hexlet-io-courses'


def test_parse_name(url, urla, default):
    assert parse_name(url, 'html') == 'python-poetry-org-docs.html'
    assert parse_name(urla, 'html') == 'en-wikipedia-org-wiki-URL.html'

    assert parse_name('https://ru.hexlet.io/packs/js/runtime.js',
                      'script') == 'ru-hexlet-io-packs-js-runtime.js'
    assert parse_name('https://ru.hexlet.io/packs/js/runtime.css',
                      'css') == 'ru-hexlet-io-packs-js-runtime.css'

    assert parse_name('/assets/professions/nodejs.png',
                      'img') == '-assets-professions-nodejs.png'
    assert parse_name('/local/templates/furniture_red/apple-icon-144x144.jpg',
                      'img') == '-local-templates-furniture'\
        '-red-apple-icon-144x144.jpg'
    assert parse_name(url, 'dir') == 'python-poetry-org-docs_files'


def test_is_equal_hostname(hexlet):
    url_false = 'https://cd23.hexlet.io/courses'
    url_true = 'https://ru.hexlet.io/data'
    assert not is_equal_hostname(hexlet, url_false)
    assert is_equal_hostname(hexlet, url_true)


def test_unificate_url(url, hexlet, default):
    assert hexlet == unificate_url(url, hexlet)
    assert urljoin(url, default) == unificate_url(url, default)
