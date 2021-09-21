# aiogram
import logging
from aiogram import Bot, Dispatcher, executor, types
# weather
import pyowm
# data base
import sqlite3
import threading
import databasemanager as db
import phrases
# time
import time
# config
import config as cfg


owm = pyowm.OWM(cfg.weatherToken, language="ru")
bot = Bot(cfg.tgToken)
dp = Dispatcher(bot)


# Создание таблицы, если нету
db.create_data_base()


def data_base_updater(message):
    id = db.select_data_base(message)
    print(id)
    insert_time = int(time.time())
    if not id:
        db.add_new_user(message, insert_time)
    else:
        db.update_user(message, id[0][0])


async def say_weather(message):
    try:
        observation = owm.weather_at_place(message.text)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')['temp']

        answer = "В городе " + message.text + " сейчас " + w.get_detailed_status() + "\n"
        answer += "На данный момент температура равна " + str(temp) + "\n\n"
        if message.text.lower() is not "привет":
            if temp < 5:
                answer += "На улице бррр холодно, одевайся в зимнее!!!"
            elif 10 > temp > 0:
                answer += "На улице холодно, одевай осеннюю курточку =) !"
            elif temp < 20:
                answer += "Немного прохладно, лучше одень кофтец и штаны!"
            else:
                answer += "Жара, так что одевайся полегче"
            await bot.send_message(message.chat.id, answer)
    except:
        await bot.send_message(message.chat.id, "Я не знаю такой город/команду, введи /help что бы узнать обо мне =)")


@dp.message_handler(commands=['start'])
async def send_start_message(message: types.Message):
    insert_time = int(time.time())
    db.add_new_user(message, insert_time)
    await bot.send_message(message.chat.id, phrases.help_Message)


@dp.message_handler(commands=['help', 'hel', 'he', 'h'])
async def send_help_message(message: types.Message):
    data_base_updater(message)
    await bot.send_message(message.chat.id, phrases.help_Message)


@dp.message_handler(commands=["kiss"])
async def send_kiss(message: types.Message):
    data_base_updater(message)
    bot.send_message(message.chat.id, "Цьом")
    bot.send_animation(message.chat.id,
                       "https://images-ext-1.discordapp.net/external/LhFcf_u-7tDiL-1KAvmAzRztPCJxYAglK5Xo8Mfsmnw/https/cdn.nekos.life/kiss/kiss_140.gif")


# приветствие
@dp.message_handler(content_types=["text"])
async def send_answer_on_text(message: types.Message):
    data_base_updater(message)
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