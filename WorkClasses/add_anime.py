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
import databasemanager as database

db = database.data_base_manager()


class scheduller_anime_updater():
	def __init__():
		pass
	def notify_user_about_new_anime(self):
		pass


class request_anime(StatesGroup):
	waiting_title = State()
	waiting_number_title = State()
	anime_titles = []
	
	def __init__(self):
		self.found_anime = {}
		self.obj_parser = yummy_parser()


	async def request_anime_title(self, bot, message, state):
		try:	
			title = message.text.split(sep=" ", maxsplit = 1)
			request_anime.anime_titles = self.obj_parser.parse(title[1])
			i = 1
			anime_list_ongoing = ""
			anime_list_not_ongoing = ""
			for anime in request_anime.anime_titles:
				if int(anime["ongoing"]) == 1:
					anime_list_ongoing += str(i)+') '+anime['name'] + '\n'
				else:
					anime_list_not_ongoing += str(i)+') '+anime['name'] + '\n'
				i+=1
			anime_list_string = "Уже вышли:\n" + anime_list_not_ongoing + "Ещё выходят:\n" + anime_list_ongoing
			await bot.send_message(message.chat.id, anime_list_string)
			await bot.send_message(message.chat.id, "введите номер аниме")
			await request_anime.waiting_number_title.set()
		except Exception:
			await bot.send_message(message.chat.id, f"Неправильное название")
			await state.finish()

		
   
	async def get_number_title(self, bot, message, state):
		try:
			number = int(message.text)
			curr_anime = request_anime.anime_titles[number-1]
			curr_anime_title = f'"{curr_anime["name"]}"'
			self.found_anime = request_anime.anime_titles[number-1]
			await bot.send_message(message.chat.id, f"Отлично, будем отслеживать:\n{curr_anime_title}")
			db.data_base_updater(message, curr_anime_title, self.obj_parser.anime_parse(self.found_anime["alias"]),
								curr_anime["ongoing"])
			await state.finish()
		except Exception:
			await bot.send_message(message.chat.id, f"Неправильный номер")
			await state.finish()
		

