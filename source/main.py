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

from work_classes.add_anime import *


bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
requester_anime = RequestAnime()


class RequestAnimeStates(StatesGroup):
    waiting_title = State()
    waiting_number_title = State()


@dp.message_handler(commands=['start'])
async def send_start_message(message: types.Message):
    insert_time = int(time.time())
    await bot.send_message(message.chat.id, phrases.help_Message)   


@dp.message_handler(commands=['help', 'hel', 'he', 'h'])
async def send_help_message(message: types.Message):
    await bot.send_message(message.chat.id, phrases.help_Message)


@dp.message_handler(commands=['search'])
async def request_anime_title(message: types.Message):   
    anime_titles = await requester_anime.request_anime_title(bot, message)
    anime_titles_string = "Finished:"
    for anime in anime_titles["not_ongoing"]:
        anime_titles_string += "\n" + anime

    anime_titles_string += "\n\nContinue:"
    for anime in anime_titles["ongoing"]:
        anime_titles_string += "\n" + anime

    await bot.send_message(message.chat.id, anime_titles_string)

    await RequestAnimeStates.waiting_number_title.set()


@dp.message_handler(state=RequestAnimeStates.waiting_number_title, content_types=types.ContentTypes.TEXT)
async def get_number_title(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "введите номер аниме")
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