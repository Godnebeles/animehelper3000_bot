#!/usr/bin/env python
# -*- coding: utf-8 -*-
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup

from YummyParser.parse import *

class request_anime(StatesGroup):
    waiting_title = State()
    waiting_number_title = State()
    anime_titles = []

    async def request_anime_title(bot, message):
        if ('/add' in str(message.text).lower()):
            title = message.text.split(sep=" ", maxsplit = 1)
            anime_list = parse(title[1])
            request_anime.anime_titles = anime_list
            anime_list_string = ''
            i = 1
            for anime in anime_list:
                anime_list_string += str(i)+') '+anime['name'] + '\n'
                i+=1

            await bot.send_message(message.chat.id, anime_list_string)
            await bot.send_message(message.chat.id, "введите номер аниме")
            await request_anime.waiting_number_title.set()
        
   
    async def get_number_title(bot,message, state):
        number = int(message.text)
        anime_list = request_anime.anime_titles
        curr_anime = anime_list[number-1]["name"]
        await bot.send_message(message.chat.id, f"Отлично, будем отслеживать:\n{curr_anime}")
        await state.finish()

