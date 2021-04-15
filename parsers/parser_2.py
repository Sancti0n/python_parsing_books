import socket
socket.setdefaulttimeout(5000)
from bs4 import BeautifulSoup
import urllib.request
import time
import json
import repackage
repackage.up()
from url import urlArraySeries, urlDomain, namePublisher

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

    for nbGenre in range(len(blockGenres[0].find_all('a'))):
        if len(blockGenres[0].find_all('a')) == nbGenre+1:
            genres = genres + str((blockGenres[0].find_all('a'))[nbGenre].getText())
        else:
            genres = genres + str((blockGenres[0].find_all('a'))[nbGenre].getText()) +", "

    dict[i] = {
        'id': i,
        'title' : (soupVolume.find('h2', class_='title')).getText(),
        'writer' : (((blockCreators.split('Writer:</dt><dd>'))[1].split('</a></dd><dt>')[0]).split('">'))[1],
        'artist' : (((blockCreators.split('Artist:</dt><dd>'))[1].split('</a></dd><dt>')[0]).split('">'))[1],
        'letterer' : ((blockCreators.split('Letterer:</dt><dd>'))[1].split('</dd><dt>')[0]),
        'translator' : ((blockCreators.split('Translator:</dt><dd>'))[1].split('</dd><dt>')[0]).replace('&amp;', '&'),
        'editor' : (((blockCreators.split('Editor:</dt><dd>'))[1].split('</a></dd><dt>')[0]).split('">'))[1],
        'cover artist' : ((((blockCreators.split('Cover Artist:</dt><dd>'))[1]).split('">')[1]).split('</a>'))[0],
        'genres' : genres,
        'date' : ((blockMeta.getText()).split('Publication Date:'))[1].split('Format:')[0].replace('\n', ''),
        'format' : ((blockMeta.getText()).split('Format:'))[1].split('Price:')[0].replace('\n', ''),
        'price' : ((blockMeta.getText()).split('Price:'))[1].split('Age range:')[0].replace('\n', ''),
        'age' : ((blockMeta.getText()).split('Age range:'))[1].split('ISBN-10:')[0].replace('\n', ''),
        'isbn-10' : ((blockMeta.getText()).split('ISBN-10:'))[1].split('ISBN-13:')[0].replace('\n', ''),
        'isbn-13' : ((blockMeta.getText()).split('ISBN-13:'))[1].split('</dd>')[0].replace('\n', '')
    }

stop = time.time()
print("The time of the run:", stop - start, "s")

with open(namePublisher[2]+'.json', 'w', encoding='utf-8') as write_file:
    json.dump(dict, write_file, ensure_ascii=False, indent=4)