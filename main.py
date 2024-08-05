import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from database import create_db_connection, save_data_in_db, close, mark_news_as_sent, get_news_from_db
from parser import load_articles_from_site

from config_reader import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
TELEGRAM_GROUP_ID = '-4202594390'
telegram_group_id = config.telegram_group_id.get_secret_value()


@dp.message(Command('start'))
async def job(message: types.Message):
    news_dict = load_articles_from_site()
    connection = create_db_connection()
    if connection:
        # Сохраняем в базу новые новости
        save_data_in_db(connection, news_dict)
    close(connection)


@dp.message(Command('news'))
async def send_news_to_telegram(message: types.Message):
    connection = create_db_connection()
    new_news = get_news_from_db(connection)
    if not new_news:
        await message.answer('Нет новых новостей для отправки')

    for id_news, title, date_time, desc, url, url_img, category in sorted(new_news):
        message = f'{date_time} {category}\n{url}'
        await bot.send_message(telegram_group_id, text=message)

        mark_news_as_sent(connection, id_news)
    close(connection)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
