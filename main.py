# aiogram
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
# data base
import sqlite3
import threading
#import databasemanager as db
import phrases
# time
import time
# config
import config as cfg
import sys
sys.path.insert(0, sys.path[0] + '/parser')
from parse import *




bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_start_message(message: types.Message):
    insert_time = int(time.time())
    await bot.send_message(message.chat.id, phrases.help_Message)


@dp.message_handler(commands=['help', 'hel', 'he', 'h'])
async def send_help_message(message: types.Message):
    await bot.send_message(message.chat.id, phrases.help_Message)

@dp.message_handler(content_types=['text'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def request_anime_title(message: types.Message):
    if ('/add' in str(message.text).lower()):
        title = message.text.split(sep=" ", maxsplit = 1)
        anime_list = parse(title[1])
        anime_list_string = ''
        i = 1
        for anime in anime_list:
            anime_list_string += str(i)+') '+anime['name'] + '\n'
            i+=1


        await bot.send_message(message.chat.id,anime_list_string)
        send = bot.send_message(message.chat.id, 'Введите номер аниме ')
        bot.register_next_step_handler(send, number_anime)


        

        number = int(message.text)
        await bot.send_message(message.chat.id,number)

        




# приветствие
@dp.message_handler(content_types=["text"])
async def send_answer_on_text(message: types.Message):
    if any(word in str(message.text).lower() for word in phrases.phrasesHello):
        await bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}")
        await bot.send_animation(message.chat.id, "https://i.gifer.com/ItBU.gif")
    elif any(word in str(message.text).lower() for word in phrases.phrasesBye):
        await bot.send_message(message.chat.id, f"Уже уходишь, {message.from_user.first_name}?")
        await bot.send_animation(message.chat.id, "https://i.gifer.com/VRhD.gif")
    else:
        await say_weather(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)