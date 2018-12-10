import requests
import json
from bs4 import BeautifulSoup

r = requests.get('https://www.foodandwine.com/recipes/spicy-sriracha-chicken-wings')
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup)