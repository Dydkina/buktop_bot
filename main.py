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

BTN_START = "/сколько"
BTN_RESET = "/Обнуляй"


@dp.message(CommandStart())
async def start(message: Message):
    # Добавляем две кнопки
    item1 = types.KeyboardButton(text=BTN_START)
    item2 = types.KeyboardButton(text=BTN_RESET)
    markup = [[item1], [item2]]

    reply = ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)
    await bot.send_message(message.chat.id, 'погнали!', reply_markup=reply)


def get_days_count_without_errors() -> int:
    date_format = '%Y-%m-%d'
    current_date = datetime.now().date()

    with open(filename, 'r') as json_file:
        json_text = json.load(json_file)
        last_date = json_text["date_of_posting"]
    days_without_errors = (current_date - datetime.strptime(last_date, date_format).date()).days

    return days_without_errors


@dp.message(Command("сколько"))
async def print_days_count_without_errors(message: types.Message) -> None:
    await bot.send_message(message.chat.id, 'дней без инцидентов {}'.format(get_days_count_without_errors()))


async def send_days_count_without_errors() -> None:
    await bot.send_message(630700190, 'дней без инцидентов {}'.format(get_days_count_without_errors()))


@dp.message(Command("Обнуляй"))
async def reset_days_without_errors(message) -> None:
    with open(filename, 'r') as json_file:
        json_text = json.load(json_file)
        json_text["date_of_reset"], json_text["date_of_posting"] = (f"{datetime.now().date()}",) * 2
        with open(filename, 'w') as json_file:
            json.dump(json_text, json_file)

    await bot.send_message(message.chat.id, '{}'.format("Обнулились"))


@dp.message(F.text)
async def handle_text(message) -> None:
    if message.text.strip() == 'ботя':
        answer = 'ты, {} - пидор'.format(message.from_user.first_name)
        await bot.send_message(message.chat.id, answer)


@dp.message()
async def send_joke():
    with open('data/fun.txt', 'r', encoding='utf-8') as file:
        last_sent_line = get_last_sent_joke_number()
        lines = file.read().split('1')
        if last_sent_line < len(lines):
            line_to_send = lines[last_sent_line].strip()
            await bot.send_message(630700190, line_to_send)
            update_last_sent_line_number(last_sent_line + 1)


def update_last_sent_line_number(line_number):
    with open('data/joke_state.txt', 'w') as state_file:
        state_file.write(str(line_number))


def get_last_sent_joke_number():
    try:
        with open('data/joke_state.txt', 'r') as state_file:
            content = state_file.read().strip()
            return int(content) if content else 0
    except FileNotFoundError:
        return 0


def on_startup() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_joke, "interval", seconds=10)
    scheduler.add_job(send_days_count_without_errors, "interval", seconds=10)
    # scheduler.add_job(send_joke, "cron", hour=15, minute=00)
    # scheduler.add_job(send_joke, "cron", hour=15, minute=00)
    scheduler.start()


async def main(bot) -> None:
    on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot))
