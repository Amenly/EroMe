# EroMe Data Scraper

This data scraper requires Python 3.8+

This scraper will download all images and videos from albums on EroMe and will allow you to scrape all albums from profile pages. If you have the required login information, you will also be able to download private albums.

![concept](images/terminal-concept.png)

# Installation

Download the latest release from the [releases page](https://github.com/Many-Trick/EroMe/releases/new).

In the command line, run the following:

`pip install -r requirements`

macOS users must use pip3:

`pip3 install -r requirements`

*Note: The config.json **must** be in the same folder as the erome.py*

# Usage

In the command line, run the following:

`python erome.py`

macOS users must use python3:

`python3 erome.py`

Once you run the script, you will be prompted for either an EroMe album link, an EroMe user profile, or a private EroMe profile. Enter the respective number and then submit a link.

If you're going to scrape a private EroMe profile, make sure to enter the email and password into the config.json.


# Options

`{"User-Agent": ""}`

You can choose to use a different user agent if you wish.

`{"folder_path": ""}`

All albums/profiles will be saved in the current working directory. Fill this field with a folder on your computer to have all content saved there instead.

`{"email": ""}`

`{"password": ""}`

These two fields must be filled in order to be able scrape private albums from profile pages. You're probably only going to be using this to scrape your *own* private albums. But who really knows for sure? ;)

# Q&A

*Note: This script was built on macOS, but I'll do my best to help Windows/Linux users.*

<details>
  <summary>Q: Why do I get an error whenever I run 'pip install -r requirements.txt'?</summary>
  <br>
  A: You either need to change your current working directory (cwd) to the directory/folder that contains the requirements.txt related to this project *or* you can just type in 'pip install -r ' in your command line and drag the requirements.txt file into the command line. If you're on macOS, remember to use pip3 instead.
</details>
  
<details>  
  <summary>Q: Why do I get an error whenever I run 'python erome.py'?</summary>
  <br>
  A: Could be the same case as the first question. Just type 'python ' or 'python3 ' and drag and drop the python script in the command line.
</details>

<details>
  <summary>Q: Why am I getting a message saying that 'config.json' couldn't be found?</summary>
  <br>
  A: Probably because you moved the 'config.json' or the 'erome.py' and they're no longer in the same folder. If you lose your config, just redownload the latest release.
</details>

<details>
  <summary>Q: Why didn't the script download all of the videos in an album?</summary>
  <br>
  A: One possibility is that some of the videos are still being encoded, in which case you'll have to scrape it again at a later time.
</details>

<details>
  <summary>Q: I received a JSONDecodeError. Help?</summary>
  <br>
  A: You're on Windows and you used backslashes instead of forward slashes for your pathname. Replace the backslashes with forward slashes.
</details>

<details>
  <summary>Q: What's a 'private EroMe profile'?</summary>
  <br>
  A: Users on EroMe have the option to have their albums set to either 'public' or 'private'. If you would like to download private albums from a user's page, you can enter that user's login details into the config file and their private albums will be downloaded. If an album is set to private but you know the album URL, you will still be able to download it using the scraper's first option.
</details>
