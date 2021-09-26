import time
import sqlite3

class data_base_manager():
	def __init__(self):
		self.conn = sqlite3.connect("database.db")
		self.cursor = self.conn.cursor()
		self.create_data_base()

	def create_data_base(self):		
		self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
					'user_id text,'
					'user_name text,'
					'anime_id text,'
					'first_name text,'
					'last_name text)')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS anime_list (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
					'anime_title text,'
					'series_count INTEGER,'
					'is_ongoing INTEGER)')
		self.conn.commit()


	def add_anime_in_db(self, message, anime_title, series_count, is_ongoing):
		self.cursor.execute(f"SELECT * FROM anime_list WHERE anime_title={anime_title}")
		self.conn.commit()
		anime = self.cursor.fetchall()
		if not anime:
			self.cursor.execute('INSERT INTO anime_list (anime_title, series_count, is_ongoing)'
					'VALUES ( '
					f'{anime_title}, {series_count}, {is_ongoing})')
			self.conn.commit()

		self.cursor.execute(f"SELECT * FROM anime_list WHERE anime_title={anime_title}")
		self.conn.commit()
		anime = self.cursor.fetchall()
		now = int(time.time())
		# time.localtime(now)
		self.cursor.execute('INSERT INTO users (user_id,'
					'user_name,'
					'first_name,'
					'last_name,'
					'anime_id)'
					'VALUES ( '
					f'"{message.from_user.id}", '
					f'"{message.from_user.username}", '
					f'"{message.from_user.first_name}", '
					f'"{message.from_user.last_name}", '
					f'{anime[0][0]})')
		self.conn.commit()


	def select_data_base(self, message):
		query = f"SELECT * FROM users WHERE user_id='{message.from_user.id}'"
		self.cursor.execute(query)
		self.conn.commit()
		return self.cursor.fetchall()


	def update_user(self, message, user, anime_title, series_count):
		now = int(time.time())
		id = user[0][0]
		print(user[0])
		anime_info = f"'{user[0][8]}{anime_title}%{series_count};'"
		query = (f'UPDATE users SET user_name="{message.from_user.username}", ' +
				f'first_name="{message.from_user.first_name}", ' +
				f'last_name="{message.from_user.last_name}" ' +
				f'WHERE id = {id}')
		print(query)
		self.cursor.execute(query)
		self.conn.commit()


	def data_base_updater(self, message, anime_title, series_count, is_ongoing):
		user = self.select_data_base(message)
		insert_time = int(time.time())
		self.add_anime_in_db(message, anime_title, series_count, is_ongoing)
