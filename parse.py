import requests
import hashlib
import sys
from bson.json_util import dumps
from bs4 import BeautifulSoup
from db import connect

# def parse():
if(len(sys.argv) < 2):
    exit('Need a url to parse information from')

r = requests.get(sys.argv[1])
soup = BeautifulSoup(r.text, 'html.parser')

#keep a hash of the summary to check if we already have it
#TODO: Improve hash to include full serialized version of recipe
db = connect()
recipes = db.recipes
data = {
    'ingredients': [],
    'instructions': [],
    'notes': [],
    'summary': '',
    'hash': ''
}

data['summary'] = soup.find('div', {'class': 'recipe-summary' }).p.text
data['hash'] = hashlib.md5(data['summary'].encode('utf-8')).hexdigest()

#if we already have that recipe, just return it to stdout
same_hash = recipes.find_one({'hash': data['hash']})
if(same_hash):
    print(dumps(same_hash))
else:
    ingredients = soup.find('div', { 'class': 'ingredients' })
    data['ingredients'] = [ li.text.strip() for li in ingredients.find_all('li') ]

    steps = soup.find_all('div', { 'class': 'step' })
    for step in steps:
        if(step.p):
            data['instructions'].append(step.p.text)
        elif(not step.div):
            data['notes'].append(step.text)
    id = recipes.insert_one(data)
    print(dumps(recipes.find_one({ '_id': id })))

#parse()
#print(dumps(recipes.find({})))
