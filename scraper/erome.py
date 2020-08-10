import os
import sys
import json
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


def check_path(path):
    if not os.path.isdir(path):
        return False


def dir_img(path):
    dir_image = path + "/Images"
    if not os.path.isdir(dir_image):
        os.mkdir(dir_image)
    return dir_image


def dir_vid(path):
    dir_video = path + "/Videos"
    if not os.path.isdir(dir_video):
        os.mkdir(dir_video)
    return dir_video


def dir_parent(url):
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        title = soup.find("h1")
        actual_title = title.text
        if "/" in actual_title:
            actual_title = actual_title.replace("/", "_")
        dir_parent = main_path + "/" + actual_title
        if not os.path.isdir(dir_parent):
            os.mkdir(dir_parent)
        return dir_parent


def dl_img(url, path):
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        images = soup.findAll("img", {"class": "img-back lasyload"})
        if len(images) == 0:
            pass
        else:
            print("Downloading images...")
        for image in tqdm(images):
            img_url = image["data-src"]
            filename = img_url.split("/")[-1]
            with requests.get(img_url) as connection:
                with open(os.path.join(dir_img(path), filename), "wb") as f:
                    f.write(connection.content)


def dl_vid(url, path):
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        videos = soup.findAll("source")
        if len(videos) == 0:
            pass
        else:
            print("Downloading videos...")
            for v in videos:
                if v not in comparison:
                    comparison.append(v)
            for video in tqdm(comparison):
                vid_url = video["src"]
                filename = vid_url.split("/")[-1]
                with requests.get(vid_url) as connection:
                    with open(os.path.join(dir_vid(path), filename), "wb") as f:
                        f.write(connection.content)


def main():
    if check_path(main_path) is False:
        print("Are you sure your path is correct? Please recheck your config")
    else:
        parent_path = dir_parent(url_user)
        dl_img(url_user, parent_path)
        dl_vid(url_user, parent_path)
        print("Done")


os.chdir(sys.path[0])

comparison = []
with open("config.json") as c:
    main_path = json.load(c)["settings"]["folder_path"]
url_user = input("Enter your link here\n > ")
if __name__ == "__main__":
    main()
