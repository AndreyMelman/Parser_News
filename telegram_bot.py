import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

from database import create_db_connection, get_news_from_db, mark_news_as_sent
from config_reader import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
TELEGRAM_GROUP_ID = '-4202594390'


@dp.message(Command('news'))
async def send_news_to_telegram(message: types.Message):
    connection = create_db_connection()
    new_news = get_news_from_db(connection)
    if not new_news:
        await message.answer('Нет новых новостей для отправки')

    for id_news, title, date_time, desc, url, url_img, category in sorted(new_news):
        message = f'{date_time} {category}\n{url}'
        await bot.send_message(TELEGRAM_GROUP_ID, text=message)

        mark_news_as_sent(connection, id_news)
    connection.close()


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
