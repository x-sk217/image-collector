import argparse
import json
import os
import urllib

from bs4 import BeautifulSoup
import requests
from termcolor import cprint

__version__ = "1.0.0"


class GoogleImageSerch(object):
    def __init__(self):
        self.GOOGLE_IMAGE_SEARCH_URL = "https://www.google.co.jp/search"
        self.session = requests.session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) \
                    Gecko/20100101 Firefox/10.0"
            }
        )

    def search(self, keyword, maximum):
        print(f"Searching {keyword}.")
        query = self.generate_query(keyword)
        return self.serch_images(query, maximum)

    def generate_query(self, keyword):
        # search query generator
        page = 0
        while True:
            params = urllib.parse.urlencode(
                {"q": keyword, "tbm": "isch", "ijn": str(page)}
            )

            yield self.GOOGLE_IMAGE_SEARCH_URL + "?" + params
            page += 1

    def serch_images(self, generate_query, maximum):
        results = []
        total = 0
        while True:
            # search
            html = self.session.get(next(generate_query)).text
            soup = BeautifulSoup(html, "lxml")
            elements = soup.select(".rg_meta.notranslate")
            jsons = [json.loads(e.get_text()) for e in elements]
            image_url_list = [js["ou"] for js in jsons]

            # add search results
            if not image_url_list:
                cprint("No more images.", "yellow")
                break
            elif len(image_url_list) > maximum - total:
                results += image_url_list[: maximum - total]
                break
            else:
                results += image_url_list
                total += len(image_url_list)

        cprint(f"Found {len(results)} images.", "green")
        return results


def main(args):
    os.makedirs(args.download_dir, exist_ok=True)
    os.makedirs(os.path.join(args.download_dir, args.target_name), exist_ok=True)

    google_image_serch = GoogleImageSerch()

    # search images
    results = google_image_serch.search(args.target_name, maximum=args.num_images)

    # download
    download_errors = []
    for i, url in enumerate(results):
        download_name = f"{(i + 1):>0{max(4, len(str(args.num_images)))}}.jpg"
        download_path = os.path.join(args.download_dir, args.target_name, download_name)

        if os.path.exists(download_path) and not args.is_overwrite:
            print(f"{download_path} is already exists.")
            download_errors.append(i + 1)
            continue

        print(f"Downloading image {download_name}.", end=" ")
        try:
            urllib.request.urlretrieve(url, download_path)
            cprint("Successful.", "green")
        except urllib.error.HTTPError:
            cprint("Failed. (HTTP Error)", "yellow")
            download_errors.append(i + 1)
            continue
        except urllib.error.URLError:
            cprint("Failed. (SSL Error)", "yellow")
            download_errors.append(i + 1)
            continue
        except UnicodeEncodeError:
            cprint("Failed. (Encoding Error)", "yellow")
            download_errors.append(i + 1)
            continue

    cprint("Download complete.", "blue")

    cprint(f"Successful: {len(results) - len(download_errors)} images.", "blue")
    if download_errors:
        cprint(f"Failed: {len(download_errors)} images.", "yellow")


if __name__ == "__main__":
    cprint("-" * 50, "magenta")
    cprint((f"Image Collector v{__version__}").center(50), "magenta")
    cprint("-" * 50, "magenta")

    parser = argparse.ArgumentParser(description=f"Image Collector v{__version__}")
    parser.add_argument(
        "-t",
        "--target",
        dest="target_name",
        help="Target name",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-n",
        "--number",
        dest="num_images",
        help="Number of images",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--directory",
        dest="download_dir",
        help="Download location",
        type=str,
        default="./data",
    )
    parser.add_argument(
        "-f",
        "--force",
        dest="is_overwrite",
        action="store_true",
        help="Whether to overwrite existing files",
    )
    args = parser.parse_args()

    main(args)
