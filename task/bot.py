from telegram_bot import start_bot, dp, telegram_group_id, tg_bot
import logging
from aiogram import types
from aiogram.filters import Command

from database import create_db_connection, get_unread_news, close, mark_news_as_sent


async def bot():
    await start_bot()


# Функция для отправки новостей в Телеграм
async def send_news_to_telegram(new_news, connection):
    list_id = []
    for id_news, title, date_time, desc, url, url_img, category in sorted(new_news):
        message = f'{date_time} {category}\n{url}'
        await tg_bot.send_message(telegram_group_id, text=message)
        list_id.append(id_news)

    mark_news_as_sent(connection, list_id)


# Функция отправки новостей
async def send_news():
    try:
        connection = create_db_connection()

        if connection:
            # Достаем новые новости, которые еще не были отправлены в Telegram
            unread_news = get_unread_news(connection)

            if unread_news:
                await send_news_to_telegram(unread_news, connection)

            # Закрываем соединение с базой
            close(connection)
    except Exception as error:
        logging.error(f'Ошибка в процессе парсинга и отправки новостей: {error}')


# Обработчик команды '/news' для ручного запуска
@dp.message(Command('news'))
async def news_handler(message: types.Message):
    await send_news()


# Обработчик команды, если нет такой писать предупреждать
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f'Такой команды нет')
