import json
import time
import urllib.request
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from url import *

def beginParsing(urlArraySeries):
    start = time.time()
    page = urllib.request.urlopen(urlArraySeries)
    soup = BeautifulSoup(page, 'html.parser')
    return start, soup

def beginParsingWithHeaders(urlArraySeries):
    start = time.time()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    page = urlopen(Request(urlArraySeries, headers=headers)).read()
    soup = BeautifulSoup(page, 'html.parser')
    return start, soup, headers

def toJson(publisher, list):
    with open(publisher+'.json', 'w', encoding='utf-8') as write_file:
        json.dump(list, write_file, ensure_ascii=False, indent=4)

def endingParsing(start):
    stop = time.time()
    print("The time of the run:", stop - start, "s")