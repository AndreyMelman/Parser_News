import logging
import asyncio

from parser.ddd_news import DddnewsNewsParser
from parser.habr_news import HabrNewsParser
from parser.onliner_news import OnlinerParse
from parser.gismeteo_news import GismeteoParse

from database import DatabaseConnection, NewsRepository


# Функция запуска парсинга сайта и записи новых новостей в базу каждые 60 мин
async def collector():
    while True:
        await parse_news()
        await asyncio.sleep(60 * 30)  # Запускать каждые 60 минут


# Функция, которая выполняет парсинг сайта и сохранение новостей в базе данных
async def parse_news():
    try:
        # Парсим сайт
        parsers = [
            DddnewsNewsParser(),
            HabrNewsParser(),
            OnlinerParse(),
            GismeteoParse()
        ]

        result = await asyncio.gather(*(article.load_articles() for article in parsers))

        # Подключаемся к базе данных
        connection = DatabaseConnection()
        connection.create_db_connection()

        # Сохраняем в базу новые новости
        news_repository = NewsRepository(connection)

        await asyncio.gather(*(news_repository.save_data_in_db(article) for article in result))

        # Закрываем соединение с базой
        connection.close_db()

    except Exception as error:
        logging.error(f'Ошибка в процессе парсинга и отправки новостей: {error}')
