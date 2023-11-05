from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv, find_dotenv
import requests

load_dotenv(find_dotenv())
storage = MemoryStorage()
bot = Bot(os.environ.get('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage)

api = os.environ.get('API_TOKEN_SALT')
response = requests.get('http://localhost:1337/api/products')
response.raise_for_status()
response_data = response.json()
products = response_data['data']

product_descriptions = {product['attributes']['title']: product['attributes']['description'] for product in products}


def get_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    for product in products:
        title = product['attributes']['title']
        kb.add(InlineKeyboardButton(title, callback_data=f'product_{title}'))
    return kb


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Добро пожаловать! Выберите товар:', reply_markup=get_kb())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('product_'))
async def process_product_callback(callback_query: types.CallbackQuery):
    product_title = callback_query.data.split('_')[1]
    description = product_descriptions.get(product_title, "Description not found")
    await bot.send_message(callback_query.from_user.id, description)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
