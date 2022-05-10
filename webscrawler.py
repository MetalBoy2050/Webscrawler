import queue
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import re
from queue import Queue


def openLink(url: str) -> None:
    patternUrlDomain = r'https?://[\w_-]+(?:(?:\.[\w_-]+)+)/'
    patternHref = r'href *= *"([^"]*)"'
    urlDomain = re.search(patternUrlDomain, url).group(0)

    queueLinks = Queue(maxsize=0)
    queueLinks.put(url)
    setLinks = {url}

    f = open('listaLinkuri.txt', 'w')

    while not queueLinks.empty():
        currLink = queueLinks.get()
        f.write(currLink)

        currText = requests.get(url).text
        currListLinks = re.findall(patternHref, currText)

        def handle_link(link: str) -> None:
            linkDomain = re.search(patternUrlDomain, link)

            if not linkDomain:
                if urlDomain + link not in setLinks:
                    response = requests.get(urlDomain + link)
                    if response.status_code == 200:
                        queueLinks.put(urlDomain + link)
                return

            linkDomain = linkDomain.group(0)

            if linkDomain != urlDomain or link in setLinks:
                return

            response = requests.get(link)
            if response.status_code == 200:
                queueLinks.put(link)

        t = time.perf_counter()
        if currListLinks:
            with ThreadPoolExecutor(max_workers=80) as pool:
                pool.map(handle_link, currListLinks)

        print(f"Time took: {time.perf_counter() - t:.2f}s")


if __name__ == '__main__':
    openLink("https://tinkerwatches.com/")
    print("something!")
