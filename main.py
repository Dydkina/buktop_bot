import json
import asyncio
import os
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
if TOKEN is None:
    raise Exception('No BOT_TOKEN env var found')

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
filename = 'data/dates.json'

# CHANNEL_NAME = '@buktop_says'

CHANNEL_NAME = '@Buktop_bot'

BTN_START = "/Начинай"
BTN_RESET = "/Обнуляй"


@dp.message(CommandStart())
async def start(message: Message):
    # Добавляем две кнопки
    item1 = types.KeyboardButton(text=BTN_START)
    item2 = types.KeyboardButton(text=BTN_RESET)
    markup = [[item1], [item2]]

    reply = ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)
    await bot.send_message(message.chat.id, 'погнали!', reply_markup=reply)


@dp.message(Command("Начинай"))
async def print_days_count_without_errors(message) -> None:
    date_format = '%Y-%m-%d'
    current_date = datetime.now().date()

    with open(filename, 'r') as json_file:
        json_text = json.load(json_file)
        last_date = json_text["date_of_posting"]

    days_without_errors = (current_date - datetime.strptime(last_date, date_format).date()).days
    await bot.send_message(message.chat.id, 'дней без инцидентов {}'.format(days_without_errors))

    # json_text["date_of_posting"] = f"{datetime.now().date()}"
    # with open(filename, 'w') as json_file:
    #     json.dump(json_text, json_file)


@dp.message(Command("Обнуляй"))
async def reset_days_without_errors(message) -> None:
    with open(filename, 'r') as json_file:
        json_text = json.load(json_file)
        json_text["date_of_reset"], json_text["date_of_posting"] = (f"{datetime.now().date()}",) * 2
        with open(filename, 'w') as json_file:
            json.dump(json_text, json_file)

    await bot.send_message(message.chat.id, '{}'.format("Обнулились"))


# def job():
#     schedule.every(10).seconds.do(print("I'm working..."))
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


@dp.message(F.text)
async def handle_text(message) -> None:
    if message.text.strip() == 'ботя':
        answer = 'ты, {} - пидор'.format(message.from_user.first_name)
        await bot.send_message(message.chat.id, answer)


@dp.message()
async def handle_text2() -> None:
    await bot.send_message(630700190, "расписание робит")


def on_startup() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(handle_text2, "interval", seconds=1)
    scheduler.start()


async def main(bot) -> None:
    on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot))
