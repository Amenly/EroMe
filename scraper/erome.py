import os
import sys
import json
import requests
from tqdm import tqdm
import concurrent.futures
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


def dir_parent_profile(url):
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        username = soup.find("div", {"class": "col-sm-5 user-info username"})
        actual_title = username.text.strip().replace("\n FOLLOW", "")
        if "/" in actual_title:
            actual_title = actual_title.replace("/", "_")
        dir_parent = main_path + "/" + actual_title
        if not os.path.isdir(dir_parent):
            os.mkdir(dir_parent)
        return dir_parent


def dir_parent_profile_album(url, path):
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        title = soup.find("h1")
        actual_title = title.text
        if "/" in actual_title:
            actual_title = actual_title.replace("/", "_")
        dir_parent = path + "/" + actual_title
        if not os.path.isdir(dir_parent):
            os.mkdir(dir_parent)
        return dir_parent


def scr_img(url):
    img_urls = []
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        images = soup.findAll("img", {"class": "img-back lasyload"})
        if len(images) == 0:
            pass
        else:
            for image in images:
                img_url = image["data-src"]
                img_urls.append(img_url)
            print(f"Downloading {len(img_urls)} images...")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                list(tqdm(executor.map(dl_img, img_urls), total=len(img_urls)))


def dl_img(url):
    with requests.get(url) as connection:
        filename = url.split("/")[-1]
        with open(os.path.join(dir_img(parent_path), filename), "wb") as f:
            f.write(connection.content)


def scr_vid(url):
    comparison = []
    vid_urls = []
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        videos = soup.findAll("source")
        if len(videos) == 0:
            pass
        else:
            for v in videos:
                if v not in comparison:
                    comparison.append(v)
            print(f"Downloading {len(comparison)} videos...")
            for video in comparison:
                vid_url = video["src"]
                vid_urls.append(vid_url)
                filename = vid_url.split("/")[-1]
            with concurrent.futures.ThreadPoolExecutor() as executor:
                list(tqdm(executor.map(dl_vid, vid_urls), total=len(vid_urls)))


def dl_vid(url):
    with requests.get(url) as connection:
        filename = url.split("/")[-1]
        with open(os.path.join(dir_vid(parent_path), filename), "wb") as f:
            f.write(connection.content)


def profile_pages(url):
    num = 0
    while 1:
        num = num + 1
        changing_url = url.format(num)
        with requests.get(changing_url) as connection:
            content = connection.content
            soup = BeautifulSoup(content, "html.parser")
            links = soup.findAll("a", {"class": "album-link"})
            if links == []:
                break
            else:
                scrape_profile_page(changing_url)


def scrape_profile_page(url):
    parent_url = url
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        links = soup.findAll("a", {"class": "album-link"})
        for link in (links):
            print("Scraping album...")
            album_link = link["href"]
            link_process_profile(album_link, parent_url)


def link_process_profile(url, p_url):
    profile_path = dir_parent_profile(p_url)
    global parent_path
    parent_path = dir_parent_profile_album(url, profile_path)
    scr_img(url)
    scr_vid(url)


def link_process(url):
    global parent_path
    parent_path = dir_parent(url)
    scr_img(url)
    scr_vid(url)


def menu():
    x = -1
    x = int(input("0 = scrape an album | 1 = scrape a profile\n> "))
    if x == 0:
        url_user = input("Enter your link here\n> ")
        link_process(url_user)
        print("Done")
    elif x == 1:
        profile_link = input("Enter the profile link here\n > ")
        profile_link = profile_link + "?page={}"
        profile_pages(profile_link)
        print("Done")


def main():
    if check_path(main_path) is False:
        print("Are you sure your path is correct? Please recheck your config.")
    else:
        menu()


os.chdir(sys.path[0])
with open("config.json") as config:
    settings = json.load(config)["settings"]
    main_path = settings["folder_path"]


if __name__ == "__main__":
    main()
