import os
import sys
import json
import requests
import concurrent.futures

from bs4 import BeautifulSoup


def text_replacement(text):
    dictionary = {'.': '_', ':': '_', '\\': '_', '/': '_'}
    for k, v in dictionary.items():
        text = text.replace(k, v)
    return text


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
        actual_title = text_replacement(actual_title)
        dir_parent = main_path + "/" + actual_title
        if not os.path.isdir(dir_parent):
            os.mkdir(dir_parent)
        return dir_parent, actual_title


def dir_parent_profile(url):
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        username = soup.find("div", {"class": "col-sm-5 user-info username"})
        actual_title = username.text.strip().replace("\n FOLLOW", "")
        actual_title = text_replacement(actual_title)
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
        actual_title = text_replacement(actual_title)
        dir_parent = path + "/" + actual_title
        if not os.path.isdir(dir_parent):
            os.mkdir(dir_parent)
        return dir_parent, actual_title


def dl_img(url, filename, index):
    try:
        with requests.get(url) as connection:
            with open(os.path.join(dir_img(parent_path), filename), "wb") as f:
                for chunk in connection.iter_content(chunk_size=50000000):
                    f.write(chunk)
        print(f"└── {filename} (✓) {index}/{length}")
    except:
        print(f"└── {filename} (✗) {index}/{length}")


def dl_vid(url, filename, index):
    try:
        with requests.get(url) as connection:
            with open(os.path.join(dir_vid(parent_path), filename), "wb") as f:
                for chunk in connection.iter_content(chunk_size=50000000):
                    f.write(chunk)
        print(f"└── {filename} (✓) {index}/{length}")
    except:
        print(f"└── {filename} (✗) {index}/{length}")


def scr_img(url, album_title):
    img_urls = []
    filenames = []
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
                filename = img_url.split("/")[-1]
                filenames.append(filename)
            global length
            length = len(img_urls)
            img_range = range(1, length + 1)
            print(f"{album_title}")
            print(f"\nDownloading {length} images...")
            print("Images")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(dl_img, img_urls, filenames, img_range)


def scr_vid(url, album_title):
    comparison = []
    vid_urls = []
    filenames = []
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
            for video in comparison:
                vid_url = video["src"]
                vid_urls.append(vid_url)
                filename = vid_url.split("/")[-1]
                filenames.append(filename)
            global length
            length = len(comparison)
            vid_range = range(1, length + 1)
            print(f"\nDownloading {length} videos...")
            print("Videos")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(dl_vid, vid_urls, filenames, vid_range)


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


def start_session(url, user_agent, email, password):
    payload = {"remember": "on"}
    payload["email"] = email
    payload["password"] = password
    headers = {}
    headers["user-agent"] = user_agent
    login_url = "https://www.erome.com/user/login"
    with requests.Session() as s:
        r = s.get(login_url, headers=headers)
        content = r.content
        soup = BeautifulSoup(content, "html.parser")
        token = soup.find("input", {"name": "_token"})["value"]
        payload["_token"] = token
        headers["referer"] = login_url
        p = s.post(login_url, data=payload, headers=headers)
        r = s.get(url)
        num = 0
        alt_url = url + "?page={}"
        while 1:
            num += 1
            changing_url = alt_url.format(num)
            r = s.get(changing_url)
            content = r.content
            soup = BeautifulSoup(content, "html.parser")
            links = soup.findAll("a", {"class": "album-link"})
            if links == []:
                break
            else:
                parent_url = changing_url
                r = s.get(changing_url)
                content = r.content
                soup = BeautifulSoup(content, "html.parser")
                links = soup.findAll("a", {"class": "album-link"})
                for link in links:
                    album_link = link["href"]
                    link_process_profile(album_link, parent_url)


def scrape_profile_page(url):
    parent_url = url
    with requests.get(url) as connection:
        content = connection.content
        soup = BeautifulSoup(content, "html.parser")
        links = soup.findAll("a", {"class": "album-link"})
        for link in links:
            album_link = link["href"]
            link_process_profile(album_link, parent_url)


def link_process_profile(url, p_url):
    profile_path = dir_parent_profile(p_url)
    global parent_path
    parent_path, actual_title = dir_parent_profile_album(url, profile_path)
    print(f"\nScraping the '{actual_title}' album...")
    scr_img(url, actual_title)
    scr_vid(url, actual_title)


def link_process(url):
    global parent_path
    parent_path, actual_title = dir_parent(url)
    print(f"\nScraping the '{actual_title}' album...")
    scr_img(url, actual_title)
    scr_vid(url, actual_title)


def menu():
    x = -1
    x = int(input(
        "0 = scrape an album | 1 = scrape a profile | 2 = scrape a private profile\n> "))
    if x == 0:
        url_user = input("Enter the album link here\n> ")
        link_process(url_user)
        print("Done")
    elif x == 1:
        profile_link = input("Enter the profile link here\n> ")
        profile_link = profile_link + "?page={}"
        profile_pages(profile_link)
        print("Done")
    elif x == 2:
        private_profile_link = input("Enter the profile link here\n> ")
        with open("config.json") as config:
            settings = json.load(config)["settings"]
            email = settings["email"]
            password = settings["password"]
            user_agent = settings["user_agent"]
        start_session(private_profile_link, user_agent, email, password)


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
