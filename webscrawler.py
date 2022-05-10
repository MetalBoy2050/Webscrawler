import urllib.request
from bs4 import BeautifulSoup
import re


def openLink(url):
    patternUrlDomain = r'https?://[\w_-]+(?:(?:\.[\w_-]+)+)/'
    pattern
    urlDomain = re.search(pattern, url).group(0)

    try:
        website = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print(e.reason)
        exit(0)

    text = website.read().decode('utf-8')
    # web = BeautifulSoup(text, 'html.parser')
    # print(web.prettify())
    listLinks = re.findall(pattern, text)
    newListLinks = []
    dictListLinks = {}

    for link in listLinks:
        linkDomain = pattern.finditer(link).group(0)

        if linkDomain != urlDomain:
            continue

        try:
            currWebsite = urllib.request.urlopen(link)
        except urllib.error.URLError as e:
            continue

        if not link.startswith(urlDomain):
            newListLinks.append(urlDomain + link)

    listLinks = newListLinks

    for link in listLinks:
        dictListLinks[link] = 1

    id = 0

    while id < len(listLinks):
        currLink = listLinks[id]

        currWebsite = urllib.request.urlopen(currLink)
        currText = currWebsite.read().decode('utf-8')
        currListLinks = re.findall(r'href *= *"([^"]*)"', currText)
        newCurrListLinks = []
        addedListLinks = []

        for link in currListLinks:
            linkDomain = pattern.finditer(link).group(0)

            if linkDomain != urlDomain:
                continue

            try:
                currWebsite = urllib.request.urlopen(link)
            except urllib.error.URLError as e:
                continue

            if not link.startswith(urlDomain):
                newCurrListLinks.append(urlDomain + link)

        for link in newCurrListLinks:
            if dictListLinks.get(link, 0) != 0:
                dictListLinks[link] = 1
                addedListLinks.append(link)

        listLinks.extend(addedListLinks)
        id += 1

    f = open("listaLinkuri.txt", "w")

    for link in listLinks:
        f.write(f'{link}\n')


if __name__ == '__main__':
    openLink("https://www.geeksforgeeks.org/")
    print("something!")
