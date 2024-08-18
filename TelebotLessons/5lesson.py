# pip install requests - установка библиотеки для отправки запросов по url алресу 
 
import telebot
import requests
import json


bot = telebot.TeleBot('7306130546:AAGX42mZ1UeEHVvwqhLJFCoRAqABnvmq-Ko')
API='04025d7a8f644339ae7f159c0656cbbb'

# Прогноз погоды
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, напиши название города!')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric') 
    if res.status_code == 200:
        data = json.loads(res.text)                                         #как обрабатывать json
        bot.reply_to(message, f'Сейчас погода: {data["main"]["temp"]}')
        temp = data["main"]["temp"]
        image = 'sun.png' if temp > 15.0 else 'rain.webp'
        file = open('./Bot1/' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, f'Не нашел такого города...')

#pip install requests - установка библиотеки
    
bot.polling(none_stop=True)

