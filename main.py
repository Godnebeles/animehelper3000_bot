# aiogram
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
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


from WorkClasses.add_anime import *


bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
requester_anime = request_anime()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Помощь по командам"),
        BotCommand(command="/add", description=" Название аниме")
    ]
    await bot.set_my_commands(commands)


@dp.message_handler(commands=['start'])
async def send_start_message(message: types.Message):
    insert_time = int(time.time())
    await bot.send_message(message.chat.id, phrases.help_Message)   


@dp.message_handler(commands=['help', 'hel', 'he', 'h'])
async def send_help_message(message: types.Message):
    await bot.send_message(message.chat.id, phrases.help_Message)


@dp.message_handler(commands=['search'])
async def request_anime_title(message: types.Message, state: FSMContext):   
    await requester_anime.request_anime_title(bot, message, state)


@dp.message_handler(state=request_anime.waiting_number_title, content_types=types.ContentTypes.TEXT)
async def get_number_title(message: types.Message, state: FSMContext):
    await requester_anime.get_number_title(bot, message, state)


# приветствие
@dp.message_handler(content_types=["text"])
async def send_answer_on_text(message: types.Message):
    if any(word in str(message.text).lower() for word in phrases.phrasesHello):
        await bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}")
        await bot.send_animation(message.chat.id, "https://i.gifer.com/ItBU.gif")
    elif any(word in str(message.text).lower() for word in phrases.phrasesBye):
        await bot.send_message(message.chat.id, f"Уже уходишь, {message.from_user.first_name}?")
        await bot.send_animation(message.chat.id, "https://i.gifer.com/VRhD.gif")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)