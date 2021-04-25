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
    subBlockPrint = blockPrint.find_all('div', class_='product-info-box__cell')
    blockInformations = soupUrlVolume.find('div', class_='l-stack l-stack--fill-last u-no-gap')
    subBlockInfo = blockInformations.find_all('div', class_='product-info-box__cell')

    author = 'Undefined'
    if re.search('byline', str(soupUrlVolume)):
        author = ((soupUrlVolume.find('p', class_='byline')).getText()).replace('By ', '')

    isbn13 = printRelease = eisbn13 = ebookRelease = 'Undefined'

    for subBlock in subBlockPrint:
        if re.search('_print_release', str(subBlock)):
            printRelease = (subBlock.find_all('span', class_='tag'))[0].getText()
        if re.search('_isbn', str(subBlock)):
            isbn13 = (subBlock.find_all('span', class_='tag'))[1].getText()
        if re.search('_ebook_release', str(subBlock)):
            ebookRelease = (subBlock.find_all('span', class_='tag'))[0].getText()
        if re.search('_eisbn', str(subBlock)):
            eisbn13 = (subBlock.find_all('span', class_='tag'))[1].getText()
    
    rating = status = formats = tags = pages = 'Undefined'
    
    for subBlock in subBlockInfo:
        if re.search('_rating', str(subBlock)):
            rating = (subBlock.find_all('span', class_='tag'))[0].getText()
        if re.search('_status', str(subBlock)):
            status = (subBlock.find_all('span', class_='tag'))[0].getText()
        if re.search('_formats', str(subBlock)):
            formats = ''
            if len(subBlock.find_all('span', class_='tag')) > 1:
                for i in range(len(subBlock.find_all('span', class_='tag'))):
                    formats = (subBlock.find_all('span', class_='tag'))[i].getText() +', '+ formats
            else:
                formats = (subBlock.find_all('span', class_='tag'))[0].getText()
        if re.search('_tags', str(subBlock)):
            tags = ''
            if len(subBlock.find_all('span', class_='tag')) > 1:
                for i in range(len(subBlock.find_all('span', class_='tag'))):
                    tags = (subBlock.find_all('span', class_='tag'))[i].getText() +', '+ tags
            else:
                tags = (subBlock.find_all('span', class_='tag'))[0].getText()
        if re.search('_pages', str(subBlock)):
            pages = (subBlock.find_all('span', class_='tag'))[0].getText()

    print(((soupUrlVolume.find('h1', class_='title title--product-page')).getText()).replace('\n  ', '').replace('\n', ''))

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
