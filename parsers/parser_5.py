import re
import urllib.request

import repackage
from bs4 import BeautifulSoup

repackage.up()
from functions import *
from url import *

start, soup = beginParsing(urlArraySeries[5])
numPage = int(((soup.find('div', class_='pagination l-cluster l-cluster--center l-cluster--end-vertical')).find_all('a'))[-2].getText().replace('\n', '').replace(' ', ''))

arrayLinksSeries = []
arrayNamesSeries = []
for i in range(1, int(numPage)+1):
    arrayLinksSeries.append(urlArraySeries[5]+'page/'+str(i))

arrayLinksVolumes = []
dict = {}
for urlLink in arrayLinksSeries:
    blockLinkSerie = urllib.request.urlopen(urlLink)
    soupUrl = BeautifulSoup(blockLinkSerie, 'html.parser')
    blockVolumes = soupUrl.find_all('h3', class_='title')

    for linkVolume in blockVolumes:
        urlVolumes = linkVolume.find_all('a', class_='card__link')

        for link in urlVolumes:
            arrayNamesSeries.append(urlDomain[4]+((link.get('href')).split('/series/')[1][:-1]))

for link in arrayNamesSeries:
    blockLinkSerie = urllib.request.urlopen(link)
    soupUrl = BeautifulSoup(blockLinkSerie, 'html.parser')
    blockVolumes = soupUrl.find_all('h3', class_='title')

    for linkVolume in blockVolumes:
        urlVolumes = linkVolume.find_all('a', class_='card__link')

        for link in urlVolumes:
            #print(link.get('href'))
            arrayLinksVolumes.append(link.get('href'))

#print(arrayLinksVolumes)
#done
'''
for i in range(len(arrayLinksVolumes)):
    blockLinkSerie = urllib.request.urlopen(arrayLinksVolumes[i])
    soupUrlVolume = BeautifulSoup(blockLinkSerie, 'html.parser')
    blockEbook = soupUrlVolume.find_all('ul', class_='l-cluster partner-links')
    blockPrint = soupUrlVolume.find('div', class_='product-info-box__release-info l-stack l-stack--fill-last u-no-gap')

    subBlockPrint = blockPrint.find_all('div', class_='product-info-box__cell')
    print(subBlockPrint)
    #for a in range(len(subBlockPrint)):
    #<div class="product-info-box__cell">

    if re.search('_isbn', str(blockPrint)):
        isbn13 = (blockPrint.find_all('span', class_='tag'))[1].getText()
    else:
        isbn13 = 'Undefined'
    if re.search('_eisbn', str(blockPrint)):
        eisbn13 = (blockPrint.find_all('span', class_='tag'))[1].getText()
    else:
        eisbn13 = 'Undefined'

    if re.search('_print_release', str(blockPrint)):
        printRelease = (blockPrint.find_all('span', class_='tag'))[0].getText()
    else:
        printRelease = 'Undefined'
    if re.search('_ebook_release', str(blockPrint)):
        ebookRelease = (blockPrint.find_all('span', class_='tag'))[0].getText()
    else:
        ebookRelease = 'Undefined'

    dict[i] = {
        'i' : i,
        'title' : (((soupUrlVolume.find('h1', class_='title title--product-page')).getText()).replace('\n  ', '').replace('\n', '')).split(', Volume')[0],
        'volume' : ((soupUrlVolume.find('h1', class_='title title--product-page')).getText()).replace('\n  ', '').replace('\n', ''),
        'author' : ((soupUrlVolume.find('p', class_='byline')).getText()).replace('By ', ''),
        #'ebook_isbn10' : ((blockEbook[1].find('a', class_='cta')).get('href')).split('/product/')[1],
        'print' : printRelease,
        'ebook release' : ebookRelease,
        'isbn13' : isbn13,
        'eisbn13' : eisbn13,
    }
print(dict)

toJson(namePublisher[5], dict)
endingParsing(start)'''