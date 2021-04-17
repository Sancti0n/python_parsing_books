import json

def toJson(publisher, list):
    with open(publisher+'.json', 'w', encoding='utf-8') as write_file:
        json.dump(list, write_file, ensure_ascii=False, indent=4)