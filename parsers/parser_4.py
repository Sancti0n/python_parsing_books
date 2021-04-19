import re
import urllib.request

import repackage
from bs4 import BeautifulSoup

repackage.up()
from functions import *
from url import *

start, soup = beginParsing(urlArraySeries[4])
blockVolumes = soup.find('div', class_='listingContainer')
linksVolumes = blockVolumes.find_all('a')
arrayLinks = []
dict = {}

for link in linksVolumes:
    if re.search('Read More', str(link)):
        arrayLinks.append(link)

for i in range(len(arrayLinks)):
    pageLink = urllib.request.urlopen(urlDomain[3]+((arrayLinks[i]).get('href'))[1:])
    soupLink = BeautifulSoup(pageLink, 'html.parser')
    blockInformations = str(soupLink.find('div', class_='floatRight'))
    blockTitle = (str(soupLink.find('div', class_='twelve columns mainArticle')).split('</h2>')[1]).split('<br')[0]
    
    if re.search('<h3>', blockTitle):
        secondTitle = (blockTitle.split('<h3>'))[1].split('</h3>')[0]
    else:
        secondTitle = ''

    if re.search('<h4>About the Book</h4>\n</div>\n<br/>\n<h3>', blockInformations):
        volume = ((blockInformations).split('<h4>About the Book</h4>\n</div>\n<br/>\n<h3>'))[1].split('</h3>')[0]
    else:
        volume = 'Undefined/One Shot'
    
    if re.search('/dp/', blockInformations):
        isbn10 = ((blockInformations.split('/dp/'))[1])[0:10] 
    if re.search('/gp/product/', blockInformations):
        isbn10 = ((blockInformations.split('/gp/product/'))[1])[0:10]
    if re.search('/ASIN/', blockInformations):
        isbn10 = ((blockInformations.split('/ASIN/'))[1])[0:10]

    dict[i] = {
        'id' : i,
        'title' : ((soupLink.find('h2')).getText()).replace('\n', ' ') + secondTitle,
        'volume' : volume,
        'author' : ((((blockInformations).split('<h4>Synopsis</h4>\n<hr/>\n<br/>\n<h4>'))[1].split('</h4>')[0]).split('<br/>')[0]).replace('<br/>\n            ', ' '),
        'date' : ((blockInformations).split('On Sale: '))[1].split('<br')[0],
        'pages' : ((blockInformations).split('Pages: '))[1].split(' ')[0],
        'isbn13' : ((blockInformations).split(' ISBN: '))[1].split('<br/>')[0],
        'isbn10' : isbn10,
        'price' : ((blockInformations).split('  MSRP: <b>'))[1].split('</b>')[0]
    }

toJson(namePublisher[4], dict)
endingParsing(start)
#The time of the run: 67.2658474445343 s
