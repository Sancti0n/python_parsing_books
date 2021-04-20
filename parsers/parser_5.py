import re
import urllib.request

import repackage
from bs4 import BeautifulSoup

repackage.up()
from functions import *
from url import *

start, soup = beginParsing(urlArraySeries[5])
numPage = int(((soup.find('div', class_='pagination l-cluster l-cluster--center l-cluster--end-vertical')).find_all('a'))[-2].getText().replace('\n', '').replace(' ', ''))
print(numPage)

arrayLinksSeries = []
for i in range(1, int(numPage)+1):
    arrayLinksSeries.append(urlArraySeries[5]+'page/'+str(i))
print(arrayLinksSeries)


'''
toJson(namePublisher[5], dict)
endingParsing(start)'''