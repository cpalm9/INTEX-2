import os
import os.path
import sys
import django
import requests
import json


os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
django.setup()

data = requests.get('http://localhost:8000/api/products/?min_price=100&category=string')
print(data.json())


data = requests.get('http://localhost:8000/api/products/?max_price=a&name=flute')
print(data.json())


data = requests.get('http://localhost:8000/api/products/?max_price=900&name=s')
print(data.json())