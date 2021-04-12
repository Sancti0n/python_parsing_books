import socket
socket.setdefaulttimeout(5000)
from bs4 import BeautifulSoup
import urllib.request
import time
import json
import repackage
repackage.up()
from url import urlArraySeries, urlDomain, namePublisher

urlPage = urlArraySeries[2]
page = urllib.request.urlopen(urlPage)
soup = BeautifulSoup(page, 'html.parser')

nbPages = ((((soup.find('span', class_='small_text')).getText()).split(' of '))[1]).split(' \xa0')[0]
arrayLinksPages = []

for i in range(1, int(nbPages)+1):
    tempUrl = urlPage[:-1]
    arrayLinksPages.append(tempUrl+str(i))
#print(arrayLinksPages)

urlLinks = soup.find_all('div', class_='list_item')

tabLink = []
for link in urlLinks:
    tabLink.append((link.find('a')).get('href'))

