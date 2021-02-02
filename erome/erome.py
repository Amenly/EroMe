import os
import sys
import concurrent.futures
import re
from collections import Counter
import argparse
import logging
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from halo import Halo


from .constants import HEADERS, LOGIN


class EroMe:
    SH_FORMAT = '%(levelname)s:%(message)s'

    def __init__(self, args, destination_path=os.getcwd(), profile_name=None,
                 album_name=None, dir_=None, cookies=None):
        self.destination_path = destination_path
        self.separate = args.separate
        self.profile_name = profile_name
        self.album_name = album_name
        self.dir = dir_
        self.cookies = cookies
        self.log = logging.getLogger(__name__)
        level = logging.DEBUG if args.debug else logging.INFO
        self.log.setLevel(level)
        if not self.log.handlers:
            formatter = logging.Formatter(fmt=self.SH_FORMAT)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.ERROR)
            stream_handler.setFormatter(formatter)
            self.log.addHandler(stream_handler)

    def handle_album(self, url):
        # pylint: disable=unbalanced-tuple-unpacking
        images, videos = self.scrape_album(url)
        album_dir = self.dir
        if self.separate:
            if images:
                self.dir = os.path.join(album_dir, 'Images')
                os.makedirs(self.dir, exist_ok=True)
                self.prepare_download(images, f'⒤: {self.album_name}')
            if videos:
                self.dir = os.path.join(album_dir, 'Videos')
                os.makedirs(self.dir, exist_ok=True)
                self.prepare_download(videos, f'⒱: {self.album_name}')
        else:
            if images or videos:
                os.makedirs(self.dir, exist_ok=True)
                self.prepare_download(images + videos)

    def scrape_album(self, item):
        if isinstance(item, str):
            url, album_name = item, None
        else:
            url, album_name = item[0], item[1]
        r = self.handle_requests(url)
        if not r:
            self.log.error(f'Unable to view album: {url}')
            return None
        if r.ok:
            soup = BeautifulSoup(r.content, 'lxml')
            if not album_name:
                self.album_name = self.clean_text(soup.h1.text)
            img_tags = soup.find_all('img', {'class': 'img-back lasyload'})
            source_tags = soup.find_all('source')
            image_urls = [tag['data-src'] for tag in img_tags]
            video_urls = [tag['src'] for tag in source_tags]
            video_urls = list(Counter(video_urls))
            if album_name:
                group = (image_urls, video_urls, album_name)
                return group
            else:
                self.dir = os.path.join(self.destination_path, self.album_name)
                return image_urls, video_urls
        else:
            self.log.error(f'Received {r.status_code} status code')

    def get_profile(self, url):
        r = self.handle_requests(url)
        if not r:
            self.log.error('Unable to view profile')
            return None
        if r.ok:
            soup = BeautifulSoup(r.content, 'lxml')
            profile_url = soup.find('a', {'id': 'user_icon'})['href']
            self.profile_name = self.clean_text(profile_url.rsplit('/', 1)[-1])
            pagination = soup.find('ul', {'class': 'pagination'})
            if pagination:
                profile_url_format = profile_url + '?page={}'
                a_tags = pagination.find_all('a')
                final_page = a_tags[-2]['href']
                final_page_number = int(final_page.rsplit('=', 1)[-1])
                list_pages = [
                    profile_url_format.format(num) for num in range(1, final_page_number + 1)
                ]
            else:
                list_pages = [url]
            return list_pages
        else:
            self.log.error(f'Received {r.status_code} status code')

    def handle_pages(self, pages):
        with Halo(text=f"Scraping {self.profile_name}'s albums...", color='magenta') as spinner:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                grouped_album_urls = list(
                    executor.map(self.get_profile_albums, pages)
                )
            combined_album_urls = [
                group for grouped_album in grouped_album_urls for group in grouped_album
            ]
            with concurrent.futures.ThreadPoolExecutor() as executor:
                media = list(
                    executor.map(self.scrape_album, combined_album_urls))
            spinner.succeed(f'Found {len(media)} albums')
        for group in media:
            *g, n = group
            self.album_name = self.clean_text(n)
            if self.separate:
                img = False
                if g[0]:
                    img = True
                    self.dir = os.path.join(
                        self.destination_path, self.profile_name, self.album_name)
                    album_dir = self.check_dir(self.dir)
                    self.dir = os.path.join(album_dir, 'Images')
                    os.makedirs(self.dir, exist_ok=True)
                    self.prepare_download(
                        g[0], f'I: {self.album_name}')
                if g[1]:
                    self.dir = os.path.join(
                        self.destination_path, self.profile_name, self.album_name)
                    if img:
                        self.dir = os.path.join(self.dir, 'Videos')
                    else:
                        album_dir = self.check_dir(self.dir)
                        self.dir = os.path.join(album_dir, 'Videos')
                    os.makedirs(self.dir, exist_ok=True)
                    self.prepare_download(
                        g[1], f'V: {self.album_name}')
            else:
                self.dir = os.path.join(
                    self.destination_path, self.profile_name, self.album_name)
                self.dir = self.check_dir(self.dir)
                os.makedirs(self.dir, exist_ok=True)
                self.prepare_download(g[0] + g[1])

    def get_profile_albums(self, url):
        r = self.handle_requests(url)
        if not r:
            self.log.error('Unable to view profile albums')
            return None
        if r.ok:
            soup = BeautifulSoup(r.content, 'lxml')
            album_links = soup.find_all('a', {'class': 'album-link'})
            album_urls = [
                (link['href'], link.div.text) for link in album_links
            ]
            return album_urls
        else:
            self.log.error(f'Received {r.status_code} status code')

    def check_dir(self, directory):
        i = 1
        while True:
            directory = self.dir
            if os.path.isdir(directory):
                directory += str(i)
                i += 1
                if os.path.isdir(directory):
                    continue
                else:
                    return directory
            else:
                return directory

    def prepare_download(self, array, desc=''):
        if not desc:
            desc = f'{self.album_name}'
        with tqdm(desc=desc, total=len(array), colour='magenta') as bar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self.download, url): url for url in array
                }
                for future in concurrent.futures.as_completed(futures):
                    future.result
                    bar.update(1)

    def download(self, url):
        filename = url.rsplit('/', 1)[-1]
        with requests.Session() as s:
            r = s.get(url, headers=HEADERS)
        if r.ok:
            with open(os.path.join(self.dir, filename), 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
        else:
            self.log.error(
                f"Received {r.status_code} status code. Could not download file '{filename}'.")
            return None

    def handle_requests(self, url, payload=None):
        with requests.Session() as s:
            if payload:
                r = s.post(url, headers=HEADERS,
                           data=payload, allow_redirects=True, cookies=self.cookies)
            else:
                r = s.get(url, headers=HEADERS,
                          allow_redirects=True, cookies=self.cookies)
            if r.ok:
                count = 1
                while count < 11:
                    pattern = re.compile(r'The site is currently')
                    match = re.search(pattern, r.text)
                    if match:
                        if payload:
                            r = s.post(
                                url, data=payload, allow_redirects=True, cookies=self.cookies)
                        else:
                            r = s.get(url, allow_redirects=True,
                                      cookies=self.cookies)
                        count += 1
                        time.sleep(5)
                        continue
                    else:
                        if not self.cookies:
                            self.cookies = r.cookies
                            if payload:
                                self.cookies = r.cookies
                        return r
                return None

    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)

    def error(self, message):
        self.log.error(message, exc_info=1)

    @staticmethod
    def clean_text(string):
        pattern = re.compile(r'[\\/:*?"<>|]')
        new_string = pattern.sub('_', string)
        return new_string


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url', type=str, help='a URL to an album or profile')
    parser.add_argument(
        '--debug', help='enables debugging for logging', action='store_true')
    parser.add_argument(
        '-s', '--separate', help='separate files by type (images/videos)', action='store_true')
    args = parser.parse_args()
    erome = EroMe(args)
    if '/a/' in args.url:
        erome.handle_album(args.url)
    else:
        pages = erome.get_profile(args.url)
        erome.handle_pages(pages)


if __name__ == '__main__':
    main()
