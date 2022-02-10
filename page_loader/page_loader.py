import argparse

from core import download_page


def main():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', default='/home/downloads/',
                        help='set output folder')
    args = parser.parse_args()
    print(download_page(args.url, content_path=args.output))


if __name__ == '__main__':
    main()
