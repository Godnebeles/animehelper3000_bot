# aiogram
import logging
from aiogram import Bot, Dispatcher, executor, types
# weather
import pyowm
# data base
import sqlite3
import threading
#import databasemanager as db
import phrases
# time
import time
# config
import config as cfg


bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_start_message(message: types.Message):
    insert_time = int(time.time())
    await bot.send_message(message.chat.id, phrases.help_Message)


@dp.message_handler(commands=['help', 'hel', 'he', 'h'])
async def send_help_message(message: types.Message):
    await bot.send_message(message.chat.id, phrases.help_Message)


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