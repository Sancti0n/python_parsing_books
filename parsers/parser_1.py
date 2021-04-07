from bs4 import BeautifulSoup
from urllib.request import urlopen, Request 
import json
import repackage
repackage.up()
from url import urlArraySeries

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

urlPage = urlArraySeries[1]
page = urlopen(Request(urlPage, headers=headers)).read()
soup = BeautifulSoup(page, 'html.parser')
blocksSeries = soup.find_all('div', class_='series-title')

arrayLinks = []

for links in blocksSeries:
    if ((links.find('a')).get('href'))[0] == '/':
        urlSerie = 'https://yenpress.com' + (links.find('a')).get('href')
    else:
        urlSerie = (links.find('a')).get('href')
    arrayLinks.append(urlSerie)