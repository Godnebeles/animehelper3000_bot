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
                   'last_message_time_to int)')
    conn.commit()


def add_new_user(message, insert_time):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    now = int(time.time())
    # time.localtime(now)
    cursor.execute('INSERT INTO users (user_id,'
                   'user_name,'
                   'first_name,'
                   'last_name,'
                   'insert_time,'
                   'last_message_time_from,'
                   'last_message_time_to)'
                   'VALUES ( '
                   f'"{message.from_user.id}", '
                   f'"{message.from_user.username}", '
                   f'"{message.from_user.first_name}", '
                   f'"{message.from_user.last_name}", '
                   f'{insert_time},{now}, {now})')
    conn.commit()


def select_data_base(message):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    sql = f"SELECT id FROM users WHERE user_id='{message.from_user.id}'"
    cursor.execute(sql)
    conn.commit()
    return cursor.fetchall()


def update_user(message, id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    now = int(time.time())
    sql = f'UPDATE users SET user_name="{message.from_user.username}", first_name="{message.from_user.first_name}", last_name="{message.from_user.last_name}", last_message_time_from={now}, last_message_time_to={now} WHERE id = {id}'
    print(sql)
    cursor.execute(sql)
    conn.commit()
