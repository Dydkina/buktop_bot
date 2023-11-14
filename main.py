import time

import json
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, types

from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram import F
from aiogram.types import Message, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# from telebot import types

TOKEN = '6315682303:AAGgmIkZD8c-Keyas7ZLiPIMudFcOexumGI'
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

filename = 'data/dates.json'

# CHANNEL_NAME = '@buktop_says'


CHANNEL_NAME = '@Buktop_bot'


# @dp.message()
# async def start() -> None:
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#
#     # Добавяем две кнопки
#     btn_name_start = "/начинай1"
#     btn_name_reset = "/Обнуляй"
#
#     item1 = types.KeyboardButton(btn_name_reset)
#     item2 = types.KeyboardButton(btn_name_start)

# markup.add(item1, item2)


@dp.message(CommandStart())
async def start(message: Message):
    # Добавляем две кнопки
    btn_name_start = "/начинай"
    btn_name_reset = "/Обнуляй"

    item1 = types.KeyboardButton(text=btn_name_reset)
    item2 = types.KeyboardButton(text=btn_name_start)
    markup = [[item1], [item2]]

    reply = ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)

    await bot.send_message(message.chat.id, 'погнали!', reply_markup=reply)


@dp.message(Command('начинай'))
async def print_days_count_without_errors(message) -> None:
    date_format = '%Y-%m-%d'
    current_date = datetime.now().date()

    with open(filename, 'r') as json_file:
        json_text = json.load(json_file)
        last_date = json_text["date_of_posting"]

    days_without_errors = (current_date - datetime.strptime(last_date, date_format).date()).days
    await bot.send_message(message.chat.id, 'дней без инцидентов {}'.format(days_without_errors))

    # data = {'date_of_posting': f"{current_date}", 'date_of_reset': f"{current_date} i"}
    json_text["date_of_posting"] = f"{datetime.now().date()}"
    with open(filename, 'w') as json_file:
        json.dump(json_text, json_file)

#
@dp.message(Command('Обнуляй'))
async def print_days_count_without_errors_yy(message) -> None:
    with open(filename, 'r') as json_file:
        json_text = json.load(json_file)
        json_text["date_of_reset"] = f"{datetime.now().date()}"
        with open(filename, 'w') as json_file:
            json.dump(json_text, json_file)

    await bot.send_message(message.chat.id, '{}'.format("Обнулились"))

@dp.message(F.text)
async def handle_text(message) -> None:
    if message.text.strip() == 'ботя':
        answer = 'ты, {} - пидор'.format(message.from_user.first_name)
        await bot.send_message(message.chat.id, answer)


# bot.send_message(CHANNEL_NAME, "Анекдоты закончились :-(")
async def main(bot) -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot))
