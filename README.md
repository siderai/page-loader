[![Tests and linter status](https://github.com/siderai/page-loader/actions/workflows/tests_and_linter_status.yml/badge.svg)](https://github.com/siderai/page-loader/actions/workflows/tests_and_linter_status.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b69cb85969106592d227/test_coverage)](https://codeclimate.com/github/siderai/page-loader/test_coverage)

# Web page downloader
A Python CLI tool that allows you to save web pages locally without a browser. The page can be properly rendered offline, as external links to assets are replaced by local paths to saved files.

## Usage:
``` bash
page-loader -h
usage: page-loader [-h] [-o OUTPUT] url

Page Loader

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        set output directory
```

## **_Codebase info_**: 

In services.py there is a bunch of internal scrapers for images, scripts and css, that download files, provided by html-soup parsing. Also, there are html parsers for file/dir's name generation.

In page_loader.py there is a high-level function "download", which saves html and related assets in specified directory. Running page_loader.py as a script will provide CLI. In case you need a direct access, the whole functionality can easily be imported to your project with "download" as a library function. 
```
├── Makefile                   - quick commands for development environment
├── README.md
├── page_loader
│   ├── __init__.py
│   ├── page_loader.py         - high-level interface, file system operations, html parsing
│   └── services.py            - bunch of scrapers for images, scripts and css
├── poetry.lock
├── pyproject.toml
├── setup.cfg
└── tests
    ├── __init__.py
    ├── fixtures
    │   ├── courses_fake.html
    │   └── courses_updated.html
    ├── test_page_loader.py   - functional tests (CLI)
    └── test_services.py      - unit tests
```

Training project at hexlet.io.

## Stack:

Python3
• pytest
• poetry
• bs4
• requests
• requests-mock
• stubs
• argparse
• urllib
• http
• logging
• git
• Linux
• Github Actions (CI)
• mypy
• flake8



## Acquired skills:
1. Web scraping using requests and bs4
2. Extending pre-built parsers with custom ones
3. Logging, debugging
4. Automating I/O bound operations (linux file system)




## Quickstart:

``` 
git clone https://github.com/siderai/page-loader
cd page-loader
make package-install
make test
page-loader --help
```

## Example:
``` 
$ page-loader https://python-poetry.org/docs/ -o ~/poetry-page
/home/siderai/poetry-page/python-poetry-org-docs.html

$ tree ~/poetry-page
/home/siderai/poetry-page
├── python-poetry-org-docs.html
└── python-poetry-org-docs_files
    ├── python-poetry-org-assets-app-ba49be1ba26bc562d8c24c3a31c0b6ca03ad61754142408ace25657cafb60d1d.js
    ├── python-poetry-org-assets-app-fa6619447c33c337b0c91325bb478f50d8fc78f85e46cd3b8be45027157c5212.css
    ├── python-poetry-org-docs-index-xml.html
    ├── python-poetry-org-docs.html
    ├── python-poetry-org-images-favicon-origami-32.png
    └── python-poetry-org-images-logo-origami.svg

1 directory, 7 files
``` 
