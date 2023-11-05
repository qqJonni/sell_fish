from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
import os
from dotenv import load_dotenv, find_dotenv
import requests
import io

load_dotenv(find_dotenv())
storage = MemoryStorage()
bot = Bot(os.environ.get('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage)

api = os.environ.get('API_TOKEN_SALT')
base_url = 'http://localhost:1337/api/products/'


def fetch_product_data(product_id):
    product_url = f'{base_url}{product_id}?populate=picture'
    response = requests.get(product_url)
    response.raise_for_status()
    response_data = response.json()

    product_data = response_data['data']['attributes']
    title = product_data['title']
    description = product_data['description']
    price = product_data['price']

    picture_data = product_data['picture']['data'][0]['attributes']
    image_relative_url = picture_data['url']
    image_url = f'http://localhost:1337{image_relative_url}'

    return {
        'title': title,
        'description': description,
        'price': price,
        'image_url': image_url
    }


def get_kb(products):
    kb = InlineKeyboardMarkup(row_width=1)
    for product in products:
        title = product['attributes']['title']
        kb.add(InlineKeyboardButton(title, callback_data=f'product_{product["id"]}'))
    return kb


def get_product_keyboard(product_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Назад", callback_data='back_to_menu'))
    return kb


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    response = requests.get(base_url)
    response.raise_for_status()
    products_data = response.json()['data']
    await message.answer('Добро пожаловать! Выберите товар:', reply_markup=get_kb(products_data))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('product_'))
async def process_product_callback(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split('_')[1])
    product_data = fetch_product_data(product_id)

    description = product_data['description']
    price = product_data['price']
    image_url = product_data['image_url']
    title = product_data['title']

    response = requests.get(image_url)
    if response.ok:
        photo_binary = response.content
        with io.BytesIO(photo_binary) as photo_stream:
            photo = InputFile(photo_stream, filename=f"{product_data['title']}.jpg")
            response_message = f"{title}\nЦена: {price}\n\n{description}"

            await bot.send_photo(callback_query.from_user.id, photo, caption=response_message, reply_markup=get_product_keyboard(product_id))


@dp.callback_query_handler(lambda c: c.data == 'back_to_menu')
async def back_to_menu(callback_query: types.CallbackQuery):
    response = requests.get(base_url)
    response.raise_for_status()
    products_data = response.json()['data']
    await bot.send_message(callback_query.from_user.id, 'Выберите товар:', reply_markup=get_kb(products_data))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
