<img src="https://raw.githubusercontent.com/Amenly/EroMe/master/images/icon-2.png" align="right">

# EroMe Data Scraper

A command line tool written in Python that will allow you to download albums on EroMe

<img src="https://raw.githubusercontent.com/Amenly/EroMe/master/images/terminal.png" align="center">

# Installation

Install `erome` by running:

```bash
$ pip install erome
```

Linux and macOS users should run:

```bash
$ pip3 install erome
```

# Usage

In order to download an album, open your CLI and type `erome` followed by a URL to an album:

```bash
$ erome https://erome.com/a/xxxxxxxx
```

You can also download all albums from a user's profile page:

```bash
$ erome https://erome.com/anonuser
```

## Flags

You can also pass in flags for additional features.

```
-h --help           Displays a list of available flags.

-s --separate       Separates files by type into their own folder. For example,
                    'Images' and 'Videos.'

-e --email          A required flag for scraping private albums from accounts. After typing
                    this, you must type that account's email address.

-p --password       A required flag for scraping private albums from accounts. After typing this,
                    you must type that account's password.
```

## Examples of using flags

If you want files to be sorted into their own folders by type:

```bash
$ erome https://erome.com/a/xxxxxxxx -s
```

If you want to scrape private albums from an account (*you must know that account's login details*):

```bash
$ erome https://erome.com/anonuser -e anonuser@gmail.com -p 1234
```

The order of the flags does not matter, and you have the option to type them out in full:

```bash
$ erome https://erome.com/anonuser --password 1234 --separate --email anonuser@gmail.com
```

# Q&A

<details>
  <summary>Q: Why didn't the script download all of the videos in an album?</summary>
  <br>
  A: One possibility is that some of the videos are still being encoded, in which case you'll have to scrape it again at a later time.
</details>

<details>
  <summary>Q: Why won't it accept my email/password?</summary>
  <br>
  A: If it's not accepting your email or your password, try wrapping them with single quotes: -e 'anonuser@gmail.com' -p '1234'
</details>
