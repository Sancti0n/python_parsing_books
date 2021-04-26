import socket

socket.setdefaulttimeout(5000)
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
arrayLinksVolumes = []
dict = {}

for i in range(1, int(numPage)+1):
    arrayLinksSeries.append(urlArraySeries[5]+'page/'+str(i))

for urlLink in arrayLinksSeries:
    blockLinkSerie = urllib.request.urlopen(urlLink)
    soupUrl = BeautifulSoup(blockLinkSerie, 'html.parser')
    blockVolumes = soupUrl.find_all('h3', class_='title')

    for linkVolume in blockVolumes:
        urlVolumes = linkVolume.find_all('a', class_='card__link')

        for link in urlVolumes:
            arrayLinksVolumes.append(link.get('href'))

for i in range(len(arrayLinksVolumes)):
    blockLinkSerie = urllib.request.urlopen(arrayLinksVolumes[i])
    soupUrlVolume = BeautifulSoup(blockLinkSerie, 'html.parser')
    blockPrint = soupUrlVolume.find('div', class_='product-info-box__release-info l-stack l-stack--fill-last u-no-gap')
    
    author = printRelease = isbn13 = ebookRelease = eisbn13 = rating = status = formats = tags = pages = 'Undefined'
    
    if blockPrint:
        subBlockPrint = blockPrint.find_all('div', class_='product-info-box__cell')
        blockInformations = soupUrlVolume.find('div', class_='l-stack l-stack--fill-last u-no-gap')
        subBlockInfo = blockInformations.find_all('div', class_='product-info-box__cell')
        
        if re.search('byline', str(soupUrlVolume)):
            author = ((soupUrlVolume.find('p', class_='byline')).getText()).replace('By ', '')
            
        for subBlock in subBlockPrint:
            if re.search('_print_release', str(subBlock)):
                printRelease = (subBlock.find_all('span', class_='tag'))[0].getText()
            if re.search('_isbn', str(subBlock)):
                isbn13 = (subBlock.find_all('span', class_='tag'))[1].getText()
            if re.search('_ebook_release', str(subBlock)):
                ebookRelease = (subBlock.find_all('span', class_='tag'))[0].getText()
            if re.search('_eisbn', str(subBlock)):
                if len(subBlock.find_all('span', class_='tag')) > 1:
                    eisbn13 = (subBlock.find_all('span', class_='tag'))[1].getText()
                else:
                    eisbn13 = (subBlock.find_all('span', class_='tag'))[0].getText()
                
        for subBlock in subBlockInfo:
            if re.search('_rating', str(subBlock)):
                rating = (subBlock.find_all('span', class_='tag'))[0].getText()
            if re.search('_status', str(subBlock)):
                status = (subBlock.find_all('span', class_='tag'))[0].getText()
            if re.search('_formats', str(subBlock)):
                if subBlock.find_all('span', class_='tag'):
                    if len(subBlock.find_all('span', class_='tag')) > 1:
                        formats = ''
                        for a in range(len(subBlock.find_all('span', class_='tag'))):
                            if (a+1) == len(subBlock.find_all('span', class_='tag')):
                                formats += (subBlock.find_all('span', class_='tag'))[a].getText()
                            else:
                                formats += (subBlock.find_all('span', class_='tag'))[a].getText() + ', '
                    else:
                        formats = (subBlock.find_all('span', class_='tag'))[0].getText()
            if re.search('_tags', str(subBlock)):
                if len(subBlock.find_all('span', class_='tag')) > 1:
                    tags = ''
                    for b in range(len(subBlock.find_all('span', class_='tag'))):
                        if (b+1) == len(subBlock.find_all('span', class_='tag')):
                            tags += (subBlock.find_all('span', class_='tag'))[b].getText()
                        else:
                            tags += (subBlock.find_all('span', class_='tag'))[b].getText() + ', '
                else:
                    tags = (subBlock.find_all('span', class_='tag'))[0].getText()
            if re.search('_pages', str(subBlock)):
                pages = (subBlock.find_all('span', class_='tag'))[0].getText()

    dict[i] = {
        'i' : i,
        'title' : (((soupUrlVolume.find('h1', class_='title title--product-page')).getText()).replace('\n  ', '').replace('\n', '')).split(', Volume')[0],
        'volume' : ((soupUrlVolume.find('h1', class_='title title--product-page')).getText()).replace('\n  ', '').replace('\n', ''),
        'author' : author,
        'print' : printRelease,
        'isbn13' : isbn13,
        'ebook release' : ebookRelease,
        'eisbn13' : eisbn13,
        'rating' : rating,
        'status' : status,
        'formats' : formats,
        'tags' : tags,
        'pages' : pages
    }

toJson(namePublisher[5], dict)
endingParsing(start)
#The time of the run: 4514.610221147537 s