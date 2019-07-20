# Image Collector

[![license](https://img.shields.io/pypi/l/git-commenter-cli.svg)](LICENSE)
[![stars](https://img.shields.io/github/stars/skmatz/image-collector.svg?style=social)](https://github.com/skmatz/image-collector/stargazers)

## Overview

This program collects images from Google Image Search.

## Description

You can download any number of images from Google Image Search.  
It will help you to collect datasets for machine learning.

## Requirement

- `Python 3.6` or higher
- `beautifulsoup4`, `requests`, `termcolor`

```bash
pip install -r requirements.txt
```

## Usage

```
--------------------------------------------------
              Image Collector v1.0.0
--------------------------------------------------
usage: image_collector.py [-h] -t TARGET_NAME -n NUM_IMAGES [-d DOWNLOAD_DIR]
                          [-f]

Image Collector v1.0.0

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_NAME, --target TARGET_NAME
                        Target name
  -n NUM_IMAGES, --number NUM_IMAGES
                        Number of images
  -d DOWNLOAD_DIR, --directory DOWNLOAD_DIR
                        Download location
  -f, --force           Whether to overwrite existing files
```

## Licence

[MIT License](./LICENSE)

## Notice

I do not assume any responsibility for copyright issues.
