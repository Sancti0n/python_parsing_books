from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
from url import tab_url

now = datetime.now()

urlpage = tab_url[0]
page = urllib.request.urlopen(urlpage)
soup = BeautifulSoup(page, 'html.parser')
block_a = soup.select("div h3 a")

tab_test = []
list_volumes = []
tab_serie = []

for link_serie in block_a:
    page_serie = urllib.request.urlopen(link_serie.get('href'))
    serie = BeautifulSoup(page_serie, 'html.parser')
    title = (serie.find("div", id="originaltitle")).get_text()
    block_volumes = serie.find_all('div', class_= "series-volume")
    tab_test.append(len(block_volumes))
    tab_serie.append(title)
    for link_volume in block_volumes:
        list_volumes.append((link_volume.find('a')).get('href'))

detail_volume = []
temporary = []
fichier = open("volume_detail_"+now.strftime("%d-%m-%Y-%H%M%S")+".txt", "a+b")

a = 0 
b = 0
c = 0
for i in range(len(list_volumes)):
    if b == 0:
        fichier.write((tab_serie[c]).encode('utf-8')+b'\n')
    page_volume = urllib.request.urlopen(list_volumes[i])
    volume = BeautifulSoup(page_volume, 'html.parser')
    fichier.write((volume.title.string).encode('utf-8')+b'\n')
    block_volume = volume.find('div', id='volume-meta')
    content_p = block_volume.find('p')
    temporary.extend([list_volumes[i], content_p])
    detail_volume.append(temporary)
    fichier.write(detail_volume[0][0].encode('utf-8')+b'\n')
    fichier.write(detail_volume[0][1].encode('utf-8')+b'\n')
    temporary[:]  = []
    if b + 1 == tab_test[a]:
        fichier.write(b'\n')
        a = a + 1
        b = 0
        c = c + 1
    else:
        b = b + 1 
fichier.close()