import time
import sqlite3


def create_data_base():
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
				   'user_id text,'
				   'user_name text,'
				   'first_name text,'
				   'last_name text,'
				   'insert_time int,'
				   'last_message_time_from int,'
				   'last_message_time_to int,'
				   'anime_list text)')
	conn.commit()


def add_new_user(message, insert_time, anime_title, series_count):
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()
	now = int(time.time())
	anime_info = f"'{anime_title}%{series_count};'"
	# time.localtime(now)
	cursor.execute('INSERT INTO users (user_id,'
				   'user_name,'
				   'first_name,'
				   'last_name,'
				   'insert_time,'
				   'last_message_time_from,'
				   'last_message_time_to,'
				   'anime_list)'
				   'VALUES ( '
				   f'"{message.from_user.id}", '
				   f'"{message.from_user.username}", '
				   f'"{message.from_user.first_name}", '
				   f'"{message.from_user.last_name}", '
				   f'{insert_time}, {now}, {now},'
				   f'{anime_info})')
	conn.commit()


def select_data_base(message):
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()
	query = f"SELECT * FROM users WHERE user_id='{message.from_user.id}'"
	cursor.execute(query)
	conn.commit()
	return cursor.fetchall()


def update_user(message, id, anime_title, series_count):
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()
	now = int(time.time())
	user = select_data_base(message)
	print(user[0])
	anime_info = f"'{user[0][8]}{anime_title}%{series_count};'"
	query = (f'UPDATE users SET user_name="{message.from_user.username}", ' +
			f'first_name="{message.from_user.first_name}", ' +
			f'last_name="{message.from_user.last_name}", ' +
			f'last_message_time_from={now}, ' +
			f'last_message_time_to={now}, ' +
			f'anime_list={anime_info} ' +
			f'WHERE id = {id}')
	print(query)
	cursor.execute(query)
	conn.commit()


def data_base_updater(message, anime_title, series_count):
	user = select_data_base(message)
	insert_time = int(time.time())
	if not user:
		add_new_user(message, insert_time, anime_title, series_count)
	else:
		update_user(message, user[0][0], anime_title, series_count)