import logging
import asyncio
from parser.ddd_news import load_articles_from_site
from database import create_db_connection, save_data_in_db, close


# Функция запуска парсинга сайта и записи новых новостей в базу каждые 60 мин
async def collector():
    while True:
        await parse_news()
        await asyncio.sleep(3600)  # Запускать каждые 60 минут


# Функция, которая выполняет парсинг сайта и сохранение новостей в базе данных
async def parse_news():
    try:
        # Парсим сайт
        news_3dnews = load_articles_from_site()
        # Подключаемся к базе данных
        connection = create_db_connection()

        if connection:
            # Сохраняем в базу новые новости
            save_data_in_db(connection, news_3dnews)
        # Закрываем соединение с базой

        close(connection)

    except Exception as error:
        logging.error(f'Ошибка в процессе парсинга и отправки новостей: {error}')
