# python -m venv.venv - устанавливаю окружение
# .venv\Scripts\activate или source .venv/bin/activate
# pip install aiogram - установка библиотеки aiogram
# pip list - проверяем устанавленные штуки

import asyncio
import logging # ввыод инфрмации в Терминал
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN # импортирую переменную из моего файла config
from aiogram.types.web_app_data import WebAppData

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hi')
    
@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Need a help?')
    
@dp.message(F.text == 'купи слона') #magic filter
async def text_memes(message: Message):
    await message.reply('Забавно')
    
@dp.message(F.photo)
async def text_photo(message: Message):
    await message.answer(f'ID фотографии: {message.photo[-1].file_id}')
    
@dp.message(Command('gimmi_photo'))
async def cmd_gimmi_photo(message: Message):
    await message.answer_photo(photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRI9MDifd0N-WyXhDj_yT0Xa4V8y5KWZHJimA&s', caption='Энштейн')
    
    
@dp.message(Command('web'))
async def cmd_web(message: Message):
    markup = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text='Web-site', web_app=types.WebAppInfo(url='https://elinavolkova.github.io/my-first-app.github.io/'))]])
    await message.answer('Open web-site', reply_markup=markup)
    
    
    
async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO) # вывод инфо в терминал, но убирать на проде
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


# python3 AiogramLessons/1srWebApp/run.py