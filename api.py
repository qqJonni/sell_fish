import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
api = os.environ.get('API_TOKEN_SALT')

response = requests.get('http://localhost:1337/api/products/2?populate=picture')
response.raise_for_status()

response_data = response.json()
products = response_data['data']

title = products['attributes']['title']
picture = products['attributes']['picture']['data'][0]['attributes']['url']

# for product in products:
#     title = product['attributes']['title']
#     # Проверьте, есть ли изображение в продукте
#     if 'picture' in product['attributes']:
#         picture_url = product['attributes']['picture'][0]['url']
#         print(f"Заголовок: {title}, URL изображения: {picture_url}")
#     else:
#         print(f"Заголовок: {title}, Нет изображения")
print(title)
print(picture)

