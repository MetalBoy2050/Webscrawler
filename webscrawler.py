from logging.handlers import QueueListener
import queue
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import re
from queue import Queue


patternUrlDomain = r'https?://[\w_-]+(?:(?:\.[\w_-]+)+)/'
patternHref = r'href *= *"([^"]*)"'
setLinks = set()
urlDomain = 2
queueLinks = Queue(maxsize=0)


def handle_link(link: str) -> None:
    linkDomain = re.search(patternUrlDomain, link)

    if not linkDomain:
        if urlDomain + link not in setLinks:
            response = requests.get(urlDomain + link)
            if response.status_code == 200:
                setLinks.add(urlDomain + link)
                queueLinks.put(urlDomain + link)
        return

    linkDomain = linkDomain.group(0)

    if linkDomain != urlDomain or link in setLinks:
        return

    response = requests.get(link)
    if response.status_code == 200:
        setLinks.add(urlDomain + link)
        queueLinks.put(link)


def handle_list_links(currListLinks):
    with ThreadPoolExecutor(max_workers=80) as pool:
        pool.map(handle_link, currListLinks)


def openLink(url: str) -> None:
    global patternUrlDomain, patternHref, setLinks, urlDomain, queueLinks
    urlDomain = re.search(patternUrlDomain, url).group(0)

    queueLinks.put(url)
    setLinks = {url}

    f = open('listaLinkuri.txt', 'w')

    while not queueLinks.empty():
        i = 0
        links = []
        listListLinks = []

        while not queueLinks.empty() and i < 10:
            link = queueLinks.get()
            text = requests.get(link).text
            listListLinks.append(re.findall(patternHref, text))
           # f.write(f'{link}\n')
            print(f'{link}')
            links.append(link)
            i += 1

        t = time.perf_counter()
        with ProcessPoolExecutor(max_workers=10) as executor:
            print("aici")
            results = executor.map(handle_list_links, listListLinks)
            for result in results:
                print("idk")
            print("end")

        print(f"Time took: {time.perf_counter() - t:.2f}s")


if __name__ == '__main__':
    openLink("https://tinkerwatches.com/")
    print("something!")
