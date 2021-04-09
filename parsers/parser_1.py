from bs4 import BeautifulSoup
from urllib.request import urlopen, Request 
import json
import repackage
repackage.up()
from url import urlArraySeries, urlDomain

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

urlPage = urlArraySeries[1]
page = urlopen(Request(urlPage, headers=headers)).read()
soup = BeautifulSoup(page, 'html.parser')
blocksSeries = soup.find_all('div', class_='series-title')

arrayLinks = []
arrayLinksVolume = []

for links in blocksSeries:
    if ((links.find('a')).get('href'))[0] == '/':
        urlSerie = urlDomain[0] + (links.find('a')).get('href')
    else:
        urlSerie = (links.find('a')).get('href')
    arrayLinks.append(urlSerie)

arrayLinksVolume = []
linksTemporary = []

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