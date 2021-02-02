<img src="https://raw.githubusercontent.com/Amenly/EroMe/master/images/icon-2.png" align="right">

# EroMe Data Scraper

![PyPI Version](https://img.shields.io/pypi/v/erome?color=%23EB75FA) ![PyPI PyVersion](https://img.shields.io/pypi/pyversions/erome?color=EB75FA)

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
```

## Examples of using flags

If you want files to be sorted into their own folders by type:

```bash
$ erome https://erome.com/a/xxxxxxxx -s
```

The order of the flags does not matter, and you have the option to type them out in full:

```bash
$ erome https://erome.com/anonuser --separate
```

# Q&A

<details>
  <summary>Q: Why didn't the script download all of the videos in an album?</summary>
  <br>
  A: One possibility is that some of the videos are still being encoded, in which case you'll have to scrape it again at a later time.
</details>