import requests
import shutil
from dateutil import parser
from bs4 import BeautifulSoup

URL_BASE = "https://app.bitcare.com"
SESSION_COOKIE = ""


def main():
    file = open("src/html/source.html")
    html = file.read()
    soup = BeautifulSoup(html)
    divs = soup.findAll("div", attrs={"class": "photo-medium"})

    for d in divs:
        dt = parser.parse(d.attrs["photo-datetime"])
        ext = d.attrs["photo-ext"]

        for c in d.children:
            try:
                s = requests.Session()
                relative = c.attrs["src"]
                relative_original = relative.replace("medium", "original")
                absolute_original = f"{URL_BASE}{relative_original}"
                r = requests.get(absolute_original, cookies={"session": SESSION_COOKIE})

                file_path = f"src/img/{dt.year}-{str(dt.month).zfill(2)}-{str(dt.day).zfill(2)}T{str(dt.hour).zfill(2)}-{str(dt.minute).zfill(2)}-{str(dt.second).zfill(2)}.{ext}"
                with open(
                    file_path,
                    "wb",
                ) as f:
                    f.write(r.content)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
