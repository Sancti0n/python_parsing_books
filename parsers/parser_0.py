import time
import urllib.request

import repackage
from bs4 import BeautifulSoup

repackage.up()
from toJSON import toJson
from url import namePublisher, urlArraySeries

start = time.time()
urlPage = urlArraySeries[0]
page = urllib.request.urlopen(urlPage)
soup = BeautifulSoup(page, 'html.parser')
urlLinks = soup.select("div h3 a")
numberArrayVolumesBySerie = []
arrayVolumes = []
arraySeries = []
informationsVolume = []
a = b = 0 
dict = {}

for linkSerie in urlLinks:
    urlSerie = urllib.request.urlopen(linkSerie.get('href'))
    serie = BeautifulSoup(urlSerie, 'html.parser')
    title = (serie.find("div", id="originaltitle")).get_text()
    arrayVolumesBySerie = serie.find_all('div', class_= "series-volume")
    numberArrayVolumesBySerie.append(len(arrayVolumesBySerie))
    arraySeries.append(title)

    for linkVolumes in arrayVolumesBySerie:
        arrayVolumes.append((linkVolumes.find('a')).get('href'))

for i in range(len(arrayVolumes)):
    linkPageVolume = urllib.request.urlopen(arrayVolumes[i])
    volume = BeautifulSoup(linkPageVolume, 'html.parser')
    contentBlockVolume = (volume.find('div', id='volume-meta')).find('p')
    informationsVolume.extend([arrayVolumes[i], contentBlockVolume])

    dict[i] = {
        'id': i,
        'title' : arraySeries[a],
        'volume' : ((volume.title.string).split('  |  '))[0],
        'editor' : ((volume.title.string).split('  |  '))[1],
        'link author': (informationsVolume[1].find('a')).get('href'),
        'author' : (informationsVolume[1].find('a')).getText(),
        'release' : ((str(informationsVolume[1]).split('<b>Release Date:</b> ')[1]).split(' <b>'))[0],
        'price' : ((str(informationsVolume[1]).split('<b>Price:</b> ')[1]).split(' <b>'))[0],
        'format' : ((str(informationsVolume[1]).split('<b>Format:</b> ')[1]).split(' <b>'))[0],
        'dimension' : ((str(informationsVolume[1]).split('<b>Trim:</b> ')[1]).split(' <b>'))[0],
        'page count' : ((str(informationsVolume[1]).split('<b>Page Count:</b> ')[1]).split(' <b>'))[0],
        'isbn' : ((str(informationsVolume[1]).split('<b>ISBN:</b> ')[1]).split('</p>'))[0]
    }
    informationsVolume[:] = []
    if b + 1 == numberArrayVolumesBySerie[a]:
        a = a + 1
        b = 0
    else:
        b = b + 1

stop = time.time()
print("The time of the run:", stop - start, "s")

toJson(namePublisher[0], dict)
