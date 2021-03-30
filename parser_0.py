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
    page_serie = urllib.request.urlopen(link_serie)
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

a = b = c = 0 

tab_info = []
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

    tab_info.append((detail_volume[0][1].find('a')).get('href'))
    author = (detail_volume[0][1].find('a')).getText()
    tab_info.append(author)
    release = str(str(detail_volume[0][1]).split('<b>Release Date:</b> ')[1]).split(' <b>')
    tab_info.append(release[0])
    price = str(str(detail_volume[0][1]).split('<b>Price:</b> ')[1]).split(' <b>')
    tab_info.append(price[0])
    format_serie = str(str(detail_volume[0][1]).split('<b>Format:</b> ')[1]).split(' <b>')
    tab_info.append(format_serie[0])
    trim = str(str(detail_volume[0][1]).split('<b>Trim:</b> ')[1]).split(' <b>')
    tab_info.append(trim[0])
    page_count = str(str(detail_volume[0][1]).split('<b>Page Count:</b> ')[1]).split(' <b>')
    tab_info.append(page_count[0])
    isbn = str(str(detail_volume[0][1]).split('<b>ISBN:</b> ')[1]).split('</p>')
    tab_info.append(isbn[0])
    fichier.write(detail_volume[0][0].encode('utf-8')+b'\n')

    for info in tab_info:
        fichier.write(info.encode('utf-8')+b'\n')
    fichier.write(b'\n')

    temporary[:]  = []
    tab_info[:]  = []
    if b + 1 == tab_test[a]:
        fichier.write(b'\n')
        a = a + 1
        b = 0
        c = c + 1
    else:
        b = b + 1 
fichier.close()