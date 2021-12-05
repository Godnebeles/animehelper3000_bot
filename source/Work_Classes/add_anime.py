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

from parser_api.source_parsers.yummy_parser import *
import db.databasemanager as database

db = database.data_base_manager()


class scheduller_anime_updater():
	def __init__():
		pass
	def notify_user_about_new_anime(self):
		pass


class RequestAnime(StatesGroup):
	anime_titles = []
	
	def __init__(self):
		self.found_anime = {}
		self.obj_parser = YummyParser()


	async def request_anime_title(self, bot, message):
		try:	
			title = message.text.split(sep=" ", maxsplit = 1)
			RequestAnime.anime_titles = self.obj_parser.parse(title[1])
			i = 1
			anime_list_ongoing = []
			anime_list_not_ongoing = []
			for anime in RequestAnime.anime_titles:
				if int(anime["ongoing"]) == 1:
					anime_list_ongoing.append(anime['name'])
				else:
					anime_list_not_ongoing.append(anime['name'])
				i+=1
			
			anime_list = {"ongoing": anime_list_ongoing, "not_ongoing" : anime_list_not_ongoing}
			return anime_list
		except Exception:
			await bot.send_message(message.chat.id, f"Неправильное название")
	
   
	async def get_number_title(self, bot, message, state):
		try:
			number = int(message.text)
			curr_anime = RequestAnime.anime_titles[number-1]
			curr_anime_title = f'"{curr_anime["name"]}"'
			self.found_anime = RequestAnime.anime_titles[number-1]
			await bot.send_message(message.chat.id, f"Отлично, будем отслеживать:\n{curr_anime_title}")
			db.data_base_updater(message, curr_anime_title, self.obj_parser.anime_parse(self.found_anime["alias"]),
								curr_anime["ongoing"])
			await state.finish()
		except Exception:
			await bot.send_message(message.chat.id, f"Неправильный номер")
			await state.finish()
		

