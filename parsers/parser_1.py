import socket

socket.setdefaulttimeout(5000)
import re
import time
from urllib.request import Request, urlopen

import repackage
from bs4 import BeautifulSoup

repackage.up()
from toJSON import toJson
from url import namePublisher, urlArraySeries, urlDomain

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
start = time.time()
urlPage = urlArraySeries[1]
page = urlopen(Request(urlPage, headers=headers)).read()
soup = BeautifulSoup(page, 'html.parser')
blocksSeries = soup.find_all('div', class_='series-title')
arrayLinks = []
arrayLinksVolume = []
linksTemporary = []
dict = {}

for links in blocksSeries:
    if ((links.find('a')).get('href'))[0] == '/':
        urlSerie = urlDomain[0] + (links.find('a')).get('href')
    else:
        urlSerie = (links.find('a')).get('href')
    arrayLinks.append(urlSerie)

for links in arrayLinks:
    urlSerie = urlopen(Request(links.replace('\n&', '&'), headers=headers)).read()
    pageSerie = BeautifulSoup(urlSerie, 'html.parser')
    blocksVolume = pageSerie.find_all('div', class_='book-format-links')

    for linkVolume in blocksVolume:
        linksTemporary = linkVolume.find_all('a')

        for var in linksTemporary:
            if ((var).get('href'))[0] == '/':
                arrayLinksVolume.append(urlDomain[0] + (var).get('href'))
            else:
                arrayLinksVolume.append((var).get('href'))            
        linksTemporary[:] = []

for i in range(len(arrayLinksVolume)):
    urlSerie = urlopen(Request(arrayLinksVolume[i], headers=headers)).read()
    pageVolume = BeautifulSoup(urlSerie, 'html.parser')
    title = (((str(pageVolume.find('h2', id='book-title')).split('>'))[1]).split('<'))[0]
    
    if re.search(', Vol. ', title):
        tempTitle = (title.split(', Vol. '))[0]
    else:
        tempTitle = 'Undefined'

    typeOfBook = 'Undefined'
    if re.search('light novel', title):
        typeOfBook = 'Light Novel'
    if re.search('manga', title):
        typeOfBook = 'Manga'

    if (len(pageVolume.find_all('span', class_='detail-value')) > 3):
        pages = (str(pageVolume.find_all('span', class_='detail-value')[3]))
    else:
        pages = 'Undefined'

    if re.search(' Pages<span>', pages):
        tempPages = ((pageVolume.find_all('span', class_='detail-value'))[3]).getText()
    else:
        tempPages = 'Undefined'

    dict[i] = {
        'id' : i,
        'title' : tempTitle,
        'number volume' : (((str(pageVolume.find('h2', id='book-title')).split('>'))[1]).split('<'))[0],
        'type of book' : typeOfBook,
        'author' : (pageVolume.find('h3', id='book-author')).getText(),
        'format book' : ((((pageVolume.find_all('span', class_='detail-key'))[0]).getText()).split('Format: '))[1],
        'pages' : tempPages,
        'isbn' : ((pageVolume.find_all('span', class_='detail-value'))[0]).getText(),
        'imprit' : ((pageVolume.find_all('span', class_='detail-value'))[1]).getText(),
        'price' : ((((pageVolume.find_all('span', class_='detail-key'))[3]).getText()).split('Price: '))[1],
        'date_mm/dd/yyyy' : ((pageVolume.find_all('span', class_='detail-value'))[2]).getText(),
        'genres' : (((str(pageVolume.find('div', id='book-categories')).split('</h4>'))[1].split('<h4>'))[0].replace('\n', '')).replace('&amp;', '&'),
        'subgenres' : (((str(pageVolume.find('div', id='book-categories')).split('</h4>'))[2].split('</div>'))[0].replace('\n', '')).replace('&amp;', '&')
    }

stop = time.time()
print("The time of the run:", stop - start, "s")
#The time of the run: 5390.788335323334 s

toJson(namePublisher[1], dict)
