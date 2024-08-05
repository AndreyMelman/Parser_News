import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from database import create_db_connection, save_data_in_db, get_news_from_db, close, mark_news_as_sent
from parser import load_articles_from_site
from config_reader import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
telegram_group_id = config.telegram_group_id.get_secret_value()


# Функция для отправки новостей в Телеграм
async def send_news_to_telegram(new_news, connection):
    for id_news, title, date_time, desc, url, url_img, category in sorted(new_news):
        message = f'{date_time} {category}\n{url}'
        await bot.send_message(telegram_group_id, text=message)

        mark_news_as_sent(connection, id_news)


# Функция, которая выполняет парсинг, сохранение и отправку новостей
async def parse_and_send_news():
    try:
        # Парсим сайт
        news_dict = load_articles_from_site()
        # Подключаемся к базе данных
        connection = create_db_connection()

        if connection:
            # Сохраняем в базу новые новости
            save_data_in_db(connection, news_dict)

            # Достаем новые новости, которые еще не были отправлены в Telegram
            new_news = get_news_from_db(connection)

            if new_news:
                await send_news_to_telegram(new_news, connection)

            # Закрываем соединение с базой
            close(connection)
    except Exception as error:
        logging.error(f'Ошибка в процессе парсинга и отправки новостей: {error}')


# Обработчик команды '/news' для ручного запуска
@dp.message(Command('news'))
async def manual_send_news(message: types.Message):
    await parse_and_send_news()


# Основная функция запуска бота
async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
