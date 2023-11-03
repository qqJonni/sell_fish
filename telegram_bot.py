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


def get_kb():
    kb = InlineKeyboardMarkup(row_width=1)

    for product in products:
        title = product['attributes']['title']
        kb.add(InlineKeyboardButton(title, callback_data='button'))

    return kb


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Добро пожаловать! Выберите товар:', reply_markup=get_kb())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
