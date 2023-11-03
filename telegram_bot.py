from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
storage = MemoryStorage()
bot = Bot(os.environ.get('TELEGRAM_TOKEN'))
dp = Dispatcher(bot, storage)


def get_kb():
  kb = InlineKeyboardMarkup(row_width=1)
  kb.add(InlineKeyboardButton('Филе сельди слабосоленой', callback_data=('btn1')),
         InlineKeyboardButton('Карп охлаждённый', callback_data=('btn2')),
         InlineKeyboardButton('Горбуша слабосоленая нарезка', callback_data=('btn3')),
         InlineKeyboardButton('Стейк сёмги свежемороженой', callback_data=('btn4')))
  return kb


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  await message.answer('Добро пожаловать! Выберите товар:', reply_markup=get_kb())


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
