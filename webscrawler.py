from threading import Thread
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor
import re


def openLink(url):
    patternUrlDomain = r'https?://[\w_-]+(?:(?:\.[\w_-]+)+)/'
    patternHref = r'href *= *"([^"]*)"'
    urlDomain = re.search(patternUrlDomain, url).group(0)

    listLinks = [url]
    setLinks = {url}

    id = 0

    while id < len(listLinks):
        currLink = listLinks[id]

        currWebsite = urllib.request.urlopen(currLink)
        currText = currWebsite.read().decode('utf-8')
        currListLinks = re.findall(patternHref, currText)
        newCurrListLinks = []
        addedListLinks = []

        for link in currListLinks:
            linkDomain = re.search(patternUrlDomain, link)

            if not linkDomain:
                try:
                    currWebsite = urllib.request.urlopen(urlDomain + link)
                    newCurrListLinks.append(urlDomain + link)
                    continue
                except urllib.error.URLError as e:
                    continue

            linkDomain = linkDomain.group(0)

            if linkDomain != urlDomain:
                continue

            try:
                currWebsite = urllib.request.urlopen(link)
                newCurrListLinks.append(link)
            except urllib.error.URLError as e:
                continue

        for link in newCurrListLinks:
            if link not in setLinks:
                setLinks.add(link)
                # f.write(f'{link}\n')
                addedListLinks.append(link)

        listLinks.extend(addedListLinks)
        id += 1

    with open('listLinkuri.txt', 'w') as f:
        for link in listLinks:
            f.write(f'{link}\n')


if __name__ == '__main__':
    openLink("https://tinkerwatches.com/")
    print("something!")
