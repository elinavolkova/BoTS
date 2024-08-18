import telebot
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot('7306130546:AAGX42mZ1UeEHVvwqhLJFCoRAqABnvmq-Ko')

@bot.message_handler(commands=['hello', 'hi'])
def main(message):
    bot.send_message(message.chat.id, f'<b>Привет!<b/>, {message.from_user.first_name}')
    
@bot.message_handler(commands=['helper'])
def main(message):
    bot.send_message(message.chat.id, message) # прописываем message.chat.id чтобы он знал куда именно отправлять сообщение
    
@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://rezka.biz/serialy/54889-i-prosto-tak.html')
    
    
    
# создание кнопок вместо клавиатуры
@bot.message_handler(commands=['buttons'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn_site1 = types.KeyboardButton('Получить комплимент')
    btn_delete2 = types.KeyboardButton('Мотивация')
    btn_edit3 = types.KeyboardButton('Нагоняй')
    markup.row(btn_site1)
    markup.row(btn_delete2, btn_edit3)
    file = open('./Bot1/12.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id, 'Что хочешь, дорогой?😇', reply_markup=markup)
    bot.register_next_step_handler(message, on_clik)

def on_clik(message):
    if message.text == 'Получить комплимент':
        bot.send_message(message.chat.id, 'Хорошо выглядишь:)')
    elif message.text == 'Мотивация':
        bot.send_message(message.chat.id, 'Никогда не сдавайся!')
    elif message.text == 'Нагоняй':
        bot.send_message(message.chat.id, 'Хватит сидеть в телефоне, иди работай')
    
    
    
# создание Inline кнопок
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn_site = types.InlineKeyboardButton('Перейти на сайт', url='https://student.skyeng.ru/onboarding/18441373/eng-adult')
    btn_delete = types.InlineKeyboardButton('Удалить сообщение', callback_data='delete')
    btn_edit = types.InlineKeyboardButton('Отредактировать сообщение', callback_data='edit')
    
    markup.row(btn_site)
    markup.row(btn_delete, btn_edit)
    bot.reply_to(message, 'Nice picture', reply_markup=markup)
    
# обработка кнопок
@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == 'edit':
        bot.edit_message_text('я лох', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'users': #это относится к блоку с создание БД
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM users')
        users = cur.fetchall() # получает то что курсор вывел
        info=''
        for i in users:
            info += f'Имя: {i[1]}, пароль: {i[2]}\n'
            
        cur.close() #закрываю курсор
        conn.close() #закрываю конэкшн
        
        bot.send_message(callback.message.chat.id, info)
        
        
        
# Создание БД
name = None # глобальная пременная

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('database.sql') # создаю подключение к БД
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, username varchar(50), pass varchar(50))') # создаем таблицу
    conn.commit() #синхронизируем курсор с коном
    cur.close() #закрываю курсор
    conn.close() #закрываю конэкшн
    
    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрируем! Введите имя')
    bot.register_next_step_handler(message, user_name) # этот метод выполняется после следующего сообщения
    
def user_name(message):
    global name
    name = message.text.strip() #strip удаляет пробелы до и после
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)
    
def user_pass(message):
    password = message.text.strip() #strip удаляет пробелы до и после
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit() #синхронизируем курсор с коном
    cur.close() #закрываю курсор
    conn.close() #закрываю конэкшн
    
    murkup = types.InlineKeyboardMarkup() # можно просто написать telebot.types 
    btn_showusers = types.InlineKeyboardButton('Список пользователей', callback_data='users')
    murkup.add(btn_showusers)

    bot.send_message(message.chat.id, 'Пользователь зарегестрирован', reply_markup=murkup)
    
# Перенесла в уже существующий раннее callback_query_handler:
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     conn = sqlite3.connect('database.sql')
#     cur = conn.cursor()
    
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall() # получает то что курсор вывел
#     info=''
#     for i in users:
#         info += f'Имя: {i[1]}, пароль: {i[2]}\n'
        
#     cur.close() #закрываю курсор
#     conn.close() #закрываю конэкшн
    
#     bot.send_message(call.message.chat.id, info) 



       
       
bot.polling(non_stop=True)

