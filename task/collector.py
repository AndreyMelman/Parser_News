import logging
import asyncio

from parser.ddd_news import load_articles_from_3dnews
from parser.habr_news import load_articles_from_habr
from parser.onliner_news import load_articles_from_onliner
from parser.gismeteo_news import load_articles_from_gismeteo

from database import DatabaseConnection, NewsRepository


# Функция запуска парсинга сайта и записи новых новостей в базу каждые 60 мин
async def collector():
    while True:
        await parse_news()
        await asyncio.sleep(60*30)  # Запускать каждые 60 минут


# Функция, которая выполняет парсинг сайта и сохранение новостей в базе данных
async def parse_news():
    try:
        # Парсим сайт
        news_3dnews = load_articles_from_3dnews()
        news_habr = load_articles_from_habr()
        news_onliner = load_articles_from_onliner()
        news_gismeteo = load_articles_from_gismeteo()
        # Подключаемся к базе данных
        connection = DatabaseConnection()
        # Сохраняем в базу новые новости
        save = NewsRepository(connection)

        save.save_data_in_db(news_3dnews)
        save.save_data_in_db(news_habr)
        save.save_data_in_db(news_onliner)
        save.save_data_in_db(news_gismeteo)

        # Закрываем соединение с базой

        connection.close_db()

    except Exception as error:
        logging.error(f'Ошибка в процессе парсинга и отправки новостей: {error}')
