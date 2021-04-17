import re
import time
import urllib.request

import repackage
from bs4 import BeautifulSoup

repackage.up()
from toJSON import toJson
from url import namePublisher, urlArraySeries, urlDomain

start = time.time()
urlPage = urlArraySeries[2]
page = urllib.request.urlopen(urlPage)
soup = BeautifulSoup(page, 'html.parser')
nbPages = ((((soup.find('span', class_='small_text')).getText()).split(' of '))[1]).split(' \xa0')[0]
arrayLinksPages = []
tabLink = []
dict = {}
genres = ""

for i in range(1, int(nbPages)+1):
    tempUrl = urlPage[:-1]
    arrayLinksPages.append(tempUrl+'='+str(i))

for links in arrayLinksPages:
    linkVolume = urllib.request.urlopen(links)
    soupUrl = BeautifulSoup(linkVolume, 'html.parser')
    urlLinks = soupUrl.find_all('div', class_='list_item')

    for link in urlLinks:
        tabLink.append((link.find('a')).get('href'))

for i in range(len(tabLink)):
    pageVolume = urllib.request.urlopen(urlDomain[1]+tabLink[i])
    soupVolume = BeautifulSoup(pageVolume, 'html.parser')
    blockCreators = str(soupVolume.find_all('div', class_='product_details'))
    blockGenres = soupVolume.find_all('div', class_='genre')
    blockMeta = soupVolume.find('div', class_='product-meta')

    print(tabLink[i])
    if re.search('Writer:</dt><dd>', blockCreators):
        writer = (((blockCreators.split('Writer:</dt><dd>'))[1].split('</a></dd><dt>')[0]).split('">'))[1]
    else:
        writer = 'Undefined'

    if re.search('Artist:</dt><dd>', blockCreators):
        artist = (((blockCreators.split('Artist:</dt><dd>'))[1].split('</a></dd><dt>')[0]).split('">'))[1]
    else:
        artist = 'Undefined'

    if re.search('Letterer:</dt><dd>', blockCreators):
        letterer = ((blockCreators.split('Letterer:</dt><dd>'))[1].split('</dd><dt>')[0])
    else:
        letterer = 'Undefined'

    if re.search('Translator:</dt><dd>', blockCreators):
        translator = ((blockCreators.split('Translator:</dt><dd>'))[1].split('</dd>')[0]).replace('&amp;', '&')
    else:
        translator = 'Undefined'

    if re.search('Editor:</dt><dd>', blockCreators):
        editor = (((blockCreators.split('Editor:</dt><dd>'))[1].split('</a></dd><dt>')[0]).split('">'))[1]
    else:
        editor = 'Undefined'

    if re.search('Cover Artist:</dt><dd>', blockCreators):
        coverArtist = ((((blockCreators.split('Cover Artist:</dt><dd>'))[1]).split('">')[1]).split('</a>'))[0]
    else:
        coverArtist = 'Undefined'

    if len(blockGenres) >= 1:
        for nbGenre in range(len(blockGenres[0].find_all('a'))):
            if len(blockGenres[0].find_all('a')) == nbGenre+1:
                genres = genres + str((blockGenres[0].find_all('a'))[nbGenre].getText())
            else:
                genres = genres + str((blockGenres[0].find_all('a'))[nbGenre].getText()) +", "
    else:
        genres = 'Undefined'
    
    if re.search('Age range:', blockMeta.getText()):
        age = ((blockMeta.getText()).split('Age range:'))[1].split('ISBN-10:')[0].replace('\n', '')
    else:
        age = 'Undefined'

    if re.search('ISBN-10:', blockMeta.getText()):
        isbn10 = ((blockMeta.getText()).split('ISBN-10:'))[1].split('ISBN-13:')[0].replace('\n', '')
    else:
        isbn10 = 'Undefined'

    if re.search('ISBN-13:', blockMeta.getText()):
        isbn13 = ((blockMeta.getText()).split('ISBN-13:'))[1].split('</dd>')[0].replace('\n', '')
    else:
        isbn13 = 'Undefined'

    dict[i] = {
        'id': i,
        'title' : (soupVolume.find('h2', class_='title')).getText(),
        'writer' : writer,
        'artist' : artist,
        'letterer' : letterer,
        'translator' : translator,
        'editor' : editor,
        'cover artist' : coverArtist,
        'genres' : genres,
        'date' : ((blockMeta.getText()).split('Publication Date:'))[1].split('Format:')[0].replace('\n', ''),
        'format' : ((blockMeta.getText()).split('Format:'))[1].split('Price:')[0].replace('\n', ''),
        'price' : ((blockMeta.getText()).split('Price:'))[1].split('Age range:')[0].replace('\n', ''),
        'age' : age,
        'isbn-10' : isbn10,
        'isbn-13' : isbn13
    }

    genres = ""

stop = time.time()
print("The time of the run:", stop - start, "s")
#The time of the run: 670.8903725147247 s

toJson(namePublisher[2], dict)
