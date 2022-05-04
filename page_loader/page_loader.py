#!/usr/bin/env
import argparse
import os
import logging
import sys

import requests
from bs4 import BeautifulSoup

from .services import save_image, save_script, save_resource, parse_name


def main(argv=None):
    parser = argparse.ArgumentParser(description="Page Loader")
    parser.add_argument("url", type=str)
    parser.add_argument(
        "-o", "--output", default=os.getcwd(), help="set output directory"
    )
    args = parser.parse_args(argv)
    try:
        print(download(args.url, content_path=args.output))
    except requests.ConnectionError:
        logging.error("Could not download the page: connection error")
    except Exception:
        logging.error(
            "Could not save to a local directory as "
            "it does not exist and cannot be created"
        )


def download(url: str, content_path: str) -> str:
    # make initial request
    request = requests.get(url)
    if request.status_code != 200:
        logging.error("Initial request failed "
                      f"with code: {request.status_code}")
        raise requests.ConnectionError
    else:
        logging.debug(f"Connection established: {url}")
    name = parse_name(url, "html")
    path = os.path.join(content_path, name)

    # prepare file system for saving assets
    content_dir_name = parse_name(url, "dir")
    path_for_files = os.path.join(content_path, content_dir_name)
    if not os.path.isdir(path_for_files):
        try:
            os.makedirs(path_for_files)
            logging.debug(f"Created assets directory: {path_for_files}")
        except PermissionError:
            logging.error(
                "Could not save to a local directory as it "
                "does not exist and cannot be created: no rights"
            )
            raise PermissionError(
                "You have no rights to create " "a directory with this path"
            )

    soup = BeautifulSoup(request.content, "html.parser")

    # save image, then replace its url by path to downloaded file
    img_items = soup.find_all("img")
    for img in img_items:
        img_path = save_image(img, path_for_files, url)
        if img_path:
            # if file is downloaded, we need to change its path to local
            img_rel_path = content_dir_name + img_path.split(
                content_dir_name)[1]
            img["src"] = img_rel_path

    # save JS files
    scripts = soup.find_all("script")
    for script in scripts:
        script_path = save_script(script, path_for_files, url)
        if script_path:
            script_rel_path = content_dir_name + script_path.split(
                content_dir_name)[1]
            script["src"] = script_rel_path

    # save CSS
    resources = soup.find_all("link")
    for res in resources:
        res_path = save_resource(res, path_for_files, url)
        if res_path:
            res_rel_path = content_dir_name + res_path.split(
                content_dir_name)[1]
            res["href"] = res_rel_path

    # save page as html locally
    with open(path, "w+") as html:
        html.write(soup.prettify())

    return path


if __name__ == "__main__":
    sys.exit(main())
