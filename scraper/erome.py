import os
import sys
import json
import concurrent.futures
import re
from collections import Counter

import requests
from bs4 import BeautifulSoup
from blessings import Terminal
from tqdm import tqdm


class Directory:
    album_directory = ""
    profile_directory = ""


def main():
    x = -1
    x = int(input(
        "0 = scrape an album | 1 = scrape a profile | 2 = scrape a private profile\n>>> "))
    if x == 0:
        url = input("Enter the album link here\n>>> ")
        link_process(url)
        print(term.magenta("Done"))
    elif x == 1:
        url = input("Enter the profile link here\n>>> ")
        scrape_profile(url)
        print(term.magenta("Done"))
    elif x == 2:
        url = input("Enter the profile link here\n>>> ")
        scrape_private_profile(url)
        print(term.magenta("Done"))


def link_process(url):
    make_dir(url)
    scrape_images(url)
    scrape_videos(url)


def make_dir(url):
    with requests.Session() as s:
        r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    title = soup.find("h1")
    album_title = text_replacement(title.text)
    if dir_profile := instance.profile_directory:
        if not os.path.isdir(dir_profile):
            os.mkdir(dir_profile)
        dir_album = dir_profile + "/" + album_title
        if not os.path.isdir(dir_album):
            os.mkdir(dir_album)
    else:
        dir_album = folder + "/" + album_title
        if not os.path.isdir(dir_album):
            os.mkdir(dir_album)
    instance.album_directory = dir_album
    print(f"\nScraping the '{term.bold(album_title)}' album...")


def text_replacement(string):
    pattern = re.compile(r'[.:/\\]')
    new_string = pattern.sub('_', string)
    return new_string


def scrape_images(url):
    with requests.Session() as s:
        r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    images = soup.findAll("img", {"class": "img-back lasyload"})
    if not images:
        pass
    else:
        image_urls = [image["data-src"] for image in images]
        len_images = len(image_urls)
        print(term.bold(f"Found {len_images} images"))
        with tqdm(total=len_images, desc="Downloading images") as bar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(
                    download_image, image_url): image_url for image_url in image_urls}
                for future in concurrent.futures.as_completed(futures):
                    future.result
                    bar.update(1)


def download_image(url):
    filename = url.split("/")[-1]
    with requests.Session() as s:
        r = s.get(url, headers=headers)
    with open(os.path.join(create_images_dir(instance.album_directory), filename), "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)


def create_images_dir(path):
    images_dir = path + "/Images"
    if not os.path.isdir(images_dir):
        os.mkdir(images_dir)
    return images_dir


def scrape_videos(url):
    with requests.Session() as s:
        r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    videos = soup.findAll("source")
    if not videos:
        pass
    else:
        videos = list(Counter(videos))
        video_urls = [video["src"] for video in videos]
        len_videos = len(videos)
        print(term.bold(f"Found {len_videos} videos"))
        with tqdm(total=len_videos, desc="Downloading videos") as bar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(
                    download_video, video_url): video_url for video_url in video_urls}
                for future in concurrent.futures.as_completed(futures):
                    future.result
                    bar.update(1)


def download_video(url):
    filename = url.split("/")[-1]
    with requests.Session() as s:
        r = s.get(url)
    with open(os.path.join(create_videos_dir(instance.album_directory), filename), "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)


def create_videos_dir(path):
    videos_dir = path + "/Videos"
    if not os.path.isdir(videos_dir):
        os.mkdir(videos_dir)
    return videos_dir


def scrape_profile(url):
    page = 0
    username = url.split("/")[-1]
    instance.profile_directory = folder + "/" + username
    url += "?page={}"
    print(f"Found {term.magenta(username)}'s profile'")
    while True:
        page += 1
        with requests.Session() as s:
            r = s.get(url.format(page))
        soup = BeautifulSoup(r.content, "lxml")
        links = soup.findAll("a", {"class": "album-link"})
        if not links:
            break
        else:
            print(term.magenta(f"\nScraping albums on page {page}..."))
            album_urls = [link["href"] for link in links]
            for album_url in album_urls:
                link_process(album_url)


def scrape_private_profile(url):
    login_url = login["referer"]
    payload = login
    page = 0
    username = url.split("/")[-1]
    instance.profile_directory = folder + "/" + username
    url += "?page={}"
    print(f"Found {term.magenta(username)}'s profile'")
    with requests.Session() as s:
        r = s.get(login_url, headers=headers)
        r.close()
        soup = BeautifulSoup(r.content, "lxml")
        token = soup.find("input", {"name": "_token"})["value"]
        payload["_token"] = token
        r = s.post(login_url, data=payload, headers=headers)
        while True:
            page += 1
            r = s.get(url.format(page))
            r.close()
            soup = BeautifulSoup(r.content, "lxml")
            links = soup.findAll("a", {"class": "album-link"})
            if not links:
                break
            else:
                print(term.magenta(f"\nScraping albums on page {page}..."))
                album_urls = [link["href"] for link in links]
                for album_url in album_urls:
                    link_process(album_url)


if __name__ == "__main__":
    config_file = sys.path[0] + "/config.json"
    with open(config_file) as f:
        config = json.load(f)["config"]
    headers = config["headers"]
    if not (folder := config["settings"]["folder_path"]):
        folder = os.getcwd()
    login = config["login"]
    instance = Directory()
    term = Terminal()
    main()
