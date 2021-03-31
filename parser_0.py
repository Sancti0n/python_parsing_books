from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
from url import urlArraySeries

now = datetime.now()

urlPage = urlArraySeries[0]
page = urllib.request.urlopen(urlPage)
soup = BeautifulSoup(page, 'html.parser')
urlLinks = soup.select("div h3 a")

numberArrayVolumesBySerie = []
arrayVolumes = []
arraySeries = []
informationsVolume = []
arrayTemporary = []

for linkSerie in urlLinks:
    urlSerie = urllib.request.urlopen(linkSerie.get('href'))
    serie = BeautifulSoup(urlSerie, 'html.parser')
    title = (serie.find("div", id="originaltitle")).get_text()
    arrayVolumesBySerie = serie.find_all('div', class_= "series-volume")
    numberArrayVolumesBySerie.append(len(arrayVolumesBySerie))
    arraySeries.append(title)
    for linkVolumes in arrayVolumesBySerie:
        arrayVolumes.append((linkVolumes.find('a')).get('href'))

fichier = open("volume_detail_"+now.strftime("%d-%m-%Y-%H%M%S")+".txt", "a+b")

a = b = c = 0 

arrayInfo = []
for i in range(len(arrayVolumes)):
    if b == 0:
        fichier.write((arraySeries[c]).encode('utf-8')+b'\n')

    linkPageVolume = urllib.request.urlopen(arrayVolumes[i])
    volume = BeautifulSoup(linkPageVolume, 'html.parser')
    fichier.write((volume.title.string).encode('utf-8')+b'\n')
    contentBlockVolume = (volume.find('div', id='volume-meta')).find('p')
    arrayTemporary.extend([arrayVolumes[i], contentBlockVolume])
    informationsVolume.append(arrayTemporary)

    #link author
    arrayInfo.append((informationsVolume[0][1].find('a')).get('href'))
    #author
    arrayInfo.append((informationsVolume[0][1].find('a')).getText())
    #release
    arrayInfo.append((str(str(informationsVolume[0][1]).split('<b>Release Date:</b> ')[1]).split(' <b>'))[0])
    #price
    arrayInfo.append((str(str(informationsVolume[0][1]).split('<b>Price:</b> ')[1]).split(' <b>'))[0])
    #format serie
    arrayInfo.append((str(str(informationsVolume[0][1]).split('<b>Format:</b> ')[1]).split(' <b>'))[0])
    #dimension
    arrayInfo.append((str(str(informationsVolume[0][1]).split('<b>Trim:</b> ')[1]).split(' <b>'))[0])
    #page count
    arrayInfo.append((str(str(informationsVolume[0][1]).split('<b>Page Count:</b> ')[1]).split(' <b>'))[0])
    #isbn
    arrayInfo.append((str(str(informationsVolume[0][1]).split('<b>ISBN:</b> ')[1]).split('</p>'))[0])
    fichier.write(informationsVolume[0][0].encode('utf-8')+b'\n')

    for info in arrayInfo:
        fichier.write(info.encode('utf-8')+b'\n')

    fichier.write(b'\n')
    arrayTemporary[:]  = []
    arrayInfo[:]  = []

    if b + 1 == numberArrayVolumesBySerie[a]:
        fichier.write(b'\n')
        a = a + 1
        b = 0
        c = c + 1
    else:
        b = b + 1

fichier.close()