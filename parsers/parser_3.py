import re
import time
import urllib.request

import repackage
from bs4 import BeautifulSoup

repackage.up()
from toJSON import toJson
from url import namePublisher, urlArraySeries, urlDomain

start = time.time()
urlPage = urlArraySeries[3]
page = urllib.request.urlopen(urlPage)
soup = BeautifulSoup(page, 'html.parser')
blockManga = (soup.find('dl', id='acMenu')).find_all('a')
arrayLinks = []
dict = {}
i = 0

for linkBook in blockManga:
    arrayLinks.append(urlDomain[2]+linkBook.get('href'))

for link in arrayLinks:
    pageLink = urllib.request.urlopen(link)
    soupLink = BeautifulSoup(pageLink, 'html.parser')
    formatBook = ((soupLink.find('div', class_='bookpage-cate')).getText()).split(' < ')[1]
    blockInformations = (soupLink.find_all('div', class_='newbook-case-detail'))

    for volume in blockInformations:
        if re.search('bookinfo', str(volume)):
            dict[i] = {
                'id' : i,
                'title' : ((volume.find('p', class_='booktitle')).getText()).split(' Volume ')[0],
                'volume' : (volume.find('p', class_='booktitle')).getText(),
                'author' : (volume.find('p', class_='author')).getText(),
                'price' : (volume.find_all('p', class_='bookinfo'))[0].getText(),
                'pages' : (volume.find_all('p', class_='bookinfo'))[1].getText(),
                'isbn13' : ((volume.find_all('p', class_='bookinfo'))[2].getText()).split('ISBN: ')[1],
                'date' : ((volume.find_all('p', class_='bookinfo'))[3].getText()).split('Published: ')[1],
                'format genre' : formatBook
            }
            i=i+1
    blockInformations[:] = []

stop = time.time()
print("The time of the run:", stop - start, "s")
#The time of the run: 114.21253252029419 s

toJson(namePublisher[3], dict)
