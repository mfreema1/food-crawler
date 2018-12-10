import requests
import hashlib
from bs4 import BeautifulSoup
from db import connect

r = requests.get('https://www.foodandwine.com/recipes/chile-garlic-chicken-wings')
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

if(recipes.count_documents({'hash': data['hash']})):
    exit('Hash of recipe already exists')

ingredients = soup.find('div', { 'class': 'ingredients' })
data['ingredients'] = [ li.text.strip() for li in ingredients.find_all('li') ]

steps = soup.find_all('div', { 'class': 'step' })
for step in steps:
    if(step.p):
        data['instructions'].append(step.p.text)
    elif(not step.div):
        data['notes'].append(step.text)

recipes.insert_one(data)
