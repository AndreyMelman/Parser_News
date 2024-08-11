from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.types import LinkPreviewOptions, Message

from telegram_bot import start_bot, telegram_group_id, bot

from database import DatabaseConnection, NewsRepository
import logging

router = Router()


async def tg_bot():
    await start_bot()


# Функция для отправки новостей в Телеграм
async def send_news_to_telegram(new_news, connection):
    mark_news = NewsRepository(connection)
    list_id = []
    for id_news, title, date_time, desc, url, url_img, category in sorted(new_news):
        options = LinkPreviewOptions(
            url=url,
            prefer_small_media=True)
        message = (f'⚡️{hbold(title)}\n\n'
                   f'💬{desc}\n\n')
        await bot.send_message(telegram_group_id, text=message, link_preview_options=options)
        list_id.append(id_news)

    mark_news.mark_news_as_sent(list_id)


# Функция отправки новостей
async def send_news():
    try:
        connection = DatabaseConnection()

        unread = NewsRepository(connection)
        if connection:
            # Достаем новые новости, которые еще не были отправлены в Telegram
            unread_news = unread.get_unread_news()

            if unread_news:
                await send_news_to_telegram(unread_news, connection)

            # Закрываем соединение с базой
            connection.close_db()
    except Exception as error:
        logging.error(f'Ошибка в процессе парсинга и отправки новостей: {error}')


# Обработчик команды '/news' для ручного запуска
@router.message(Command('news'))
async def news_handler(message: Message):
    await send_news()


# Обработчик команды, если нет такой писать предупреждать
@router.message()
async def echo_handler(message: Message):
    await message.answer(f'Такой команды нет')
