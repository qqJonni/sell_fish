import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
api = os.environ.get('API_TOKEN_SALT')

response = requests.get('http://localhost:1337/api/products')
response.raise_for_status()

response_data = response.json()
products = response_data['data']

for product in products:
    title = product['attributes']['title']
    print(title)
