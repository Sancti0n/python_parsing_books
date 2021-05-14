import repackage
import json
repackage.up()

from functions import *
from url import *

# id de votre profil Bubble
# https://www.appbubble.co/user/{id}/ma-collection
site = 'https://api.appbubble.co/v1.3/libraries/'
idBubble = ''

page = urllib.request.urlopen(site+idBubble)
soup = BeautifulSoup(page, 'html.parser')

# Pour enregistrer le json localement
# with open('Bubble_list.json', 'w', encoding='utf-8') as write_file:
#   json.dump(json.loads(str(soup)), write_file, ensure_ascii=False, indent=4)


# Pour naviguer dans le json :

# jsonSerialized = json.loads(str(soup))
# Si vous voulez un id précis :
# json.dumps(jsonSerialized[{id}], indent=4)
# Pour avoir le maximum de jsonSerialized : len(jsonSerialized)
# Pour naviguer dans la partie série : 
# json.dumps(jsonSerialized[{id}]['serie'], indent=4)
# Pour naviguer dans une partie de série, title par exemple :
# json.dumps(jsonSerialized[{id}]['serie']['title'], indent=4)