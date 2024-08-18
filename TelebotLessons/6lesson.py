# pip install CurrencyConverter - установка библиотеки для конвертации валют
 
import telebot
from currency_converter import CurrencyConverter
from telebot import types


bot = telebot.TeleBot('7306130546:AAGX42mZ1UeEHVvwqhLJFCoRAqABnvmq-Ko')
currency = CurrencyConverter() # конвертер
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введи сумму')
    bot.register_next_step_handler(message, summa)
    
def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, введите число')
        bot.register_next_step_handler(message, summa)
        return # следующий код не выполняется
    
    if amount>0:
        marckup=types.InlineKeyboardMarkup(row_width=2) # 2 кнопки в ряду
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        marckup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=marckup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0, введите сумму')
        bot.register_next_step_handler(message, summa)
        
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'{amount} {values[0]} = {round(res, 2)} {values[1]}. Введите новую сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару валют через /')
        bot.register_next_step_handler(call.message, mycurrency)

def mycurrency(message):
    try:
        values = message.text.strip().upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'{amount} {values[0]} = {round(res, 2)} {values[1]}. Введите новую сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Введите валюты в таком формате: USD/EUR')
        bot.register_next_step_handler(message, mycurrency)
            


bot.polling(none_stop=True)