import urllib.request
from bs4 import BeautifulSoup
import re


def openLink(url):
    patternUrlDomain = r'https?://[\w_-]+(?:(?:\.[\w_-]+)+)/'
    patternHref = r'href *= *"([^"]*)"'
    urlDomain = re.search(patternUrlDomain, url).group(0)
    print(urlDomain)

    try:
        website = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print(e.reason)
        exit(0)

    text = website.read().decode('utf-8')
    # web = BeautifulSoup(text, 'html.parser')
    # print(web.prettify())
    listLinks = re.findall(patternHref, text)
    newListLinks = []
    dictListLinks = {}

    f = open("listaLinkuri.txt", "w")

    for link in listLinks:
        linkDomain = re.search(patternUrlDomain, link)

        if not linkDomain:
            try:
                currWebsite = urllib.request.urlopen(urlDomain + link)
                newListLinks.append(urlDomain + link)
                continue
            except urllib.error.URLError as e:
                continue

        linkDomain = linkDomain.group(0)

        if linkDomain != urlDomain:
            continue

        try:
            currWebsite = urllib.request.urlopen(link)
            newListLinks.append(link)
        except urllib.error.URLError as e:
            continue

    listLinks = newListLinks

    for link in listLinks:
        f.write(f'{link}\n')
        dictListLinks[link] = 1

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
                    newListLinks.append(urlDomain + link)
                    continue
                except urllib.error.URLError as e:
                    continue

            linkDomain = linkDomain.group(0)

            if linkDomain != urlDomain:
                continue

            try:
                currWebsite = urllib.request.urlopen(link)
                newListLinks.append(link)
            except urllib.error.URLError as e:
                continue

        for link in newCurrListLinks:
            if not dictListLinks.get(link, 0):
                dictListLinks[link] = 1
                f.write(f'{link}\n')
                addedListLinks.append(link)

        listLinks.extend(addedListLinks)
        id += 1

    for link in listLinks:
        f.write(f'{link}\n')


if __name__ == '__main__':
    openLink("https://tinkerwatches.com/")
    print("something!")
