#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import logging
from aiogram import Bot, Dispatcher, executor, types
import markup as nav
import sqlite3

API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#создание БД и таблици для users
connect = sqlite3.connect(r'sqlite3/all_info.db')
cur = connect.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users_info 
    (
    id_user TEXT,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    language_code TEXT,
    date_register TEXT
    );
    """)
connect.commit()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Информация о пользователе.
    id_user = str(message.from_user.id)
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name 
    username = message.from_user.username
    language_code = message.from_user.language_code
    date_user = message.date

    file = open("userlog.txt", "a")
    file.write(f"{message.date} id - ({message.from_user.id} {message.from_user.first_name} {message.from_user.last_name }) ({message.text})\n")
    file.close() 

    try:
        db = sqlite3.connect(r'sqlite3/all_info.db')
        cur = db.cursor()
        exept_info = cur.execute('SELECT * FROM users_info  WHERE id_user=?', (id_user, ))

        if exept_info.fetchone() is None: 
            #регистрация
            row = (id_user, first_name, last_name, username, language_code, date_user)
            cur.execute("INSERT INTO users_info VALUES(?, ?, ?, ?, ?, ?);", row)
        else:
            
            #sms  = (f"Welcom {first_name} {last_name}")
            #await message.reply(sms, reply_markup = nav.mainMenu)
            pass
        #пример для использования мультиязычного описания
        if language_code == "ru" or language_code == "ua":
            text = open('text/start.txt')
            text_start = text.read()
        else:
            text = open('text/start_en.txt')
            text_start = text.read()
        await message.reply(text_start, reply_markup = nav.mainMenu)
        db.commit()
    except sqlite3.Error as e:
        if con: con.rollback()
        print("Error work in SQLite3", e)
    finally:
        if db:
            cur.close()
            #print("Connect SQLite3 close")

    #проверить создан ли акаунт в БД если нет создать, и поприветствовать с входом.

@dp.message_handler()
async def echo(message: types.Message):
    #await message.answer(message.text)
    db = sqlite3.connect(r'sqlite3/all_info.db')
    cur = db.cursor()
    exept_info = cur.execute('SELECT * FROM users_info  WHERE id_user=?', (message.from_user.id, ))
    #print(f"{message}")
    if exept_info.fetchone() is None: 
        #регистрация в случае добавления бота без старта
        row = (str(message.from_user.id), message.from_user.first_name, message.from_user.last_name, message.from_user.language_code, message.date)
        cur.execute("INSERT INTO users_info VALUES(?, ?, ?, ?, ?, ?);", row)
    elif int(message.from_user.id) > 0:
        if message.text == "/Graphics":    
            
            file = open("userlog.txt", "a")
            file.write(f"{message.date} id - ({message.from_user.id} {message.from_user.first_name} {message.from_user.last_name }) ({message.text})\n")
            file.close()   
           
            text = open('info_orders.txt')
            text_help = text.read()
            await bot.send_photo(message.chat.id, types.InputFile('orders.png'))
            await message.answer(text_help, reply_markup = nav.mainMenu)
        elif message.text == "/Text":

            file = open("userlog.txt", "a")
            file.write(f"{message.date} id - ({message.from_user.id} {message.from_user.first_name} {message.from_user.last_name }) ({message.text})\n")
            file.close()   
           
            text = open('orders.txt')
            text_help = text.read()
            await message.answer(text_help, reply_markup = nav.mainMenu)
        elif message.text == "/Development_plan":
            file = open("userlog.txt", "a")
            file.write(f"{message.date} id - ({message.from_user.id} {message.from_user.first_name} {message.from_user.last_name }) ({message.text})\n")
            file.close() 

            text = open('text/Development_plan.txt')
            text_help = text.read()
            await message.answer(text_help, reply_markup = nav.mainMenu)
        elif message.text == "/Info":
           
            file = open("userlog.txt", "a")
            file.write(f"{message.date} id - ({message.from_user.id} {message.from_user.first_name} {message.from_user.last_name }) ({message.text})\n")
            file.close() 
           
            text = open('text/Info.txt')
            text_help = text.read()
            await message.answer(text_help, reply_markup = nav.mainMenu)
        else:
            await message.reply("I don't have such command.")
    db.commit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
