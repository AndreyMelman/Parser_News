import json
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import psycopg2
from config import host, user, password, db_name
import os
import schedule


# Функция парсинга новостного сайта
def load_articles_from_site():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/127.0.0.0 Safari/537.36'
    }
    url = 'https://3dnews.ru/software-news/rss'
    # Получаем URL нашего сайта
    response = requests.get(url, headers=headers)
    # Получаем HTML-файл
    soup = BeautifulSoup(response.content, 'xml')
    # Получаем кусок HTML-файла с которого будем парсить новости
    articles_items = soup.find_all('item')

    # Создаем словарь для записи новостей
    news_dict = {}

    for article in articles_items:
        article_title = article.find('title').text
        article_url = article.find('link').text
        article_id = article.find('link').text.split('/')[3]
        article_desc = article.find('description').text
        article_img_url = article.find('enclosure').get('url')
        article_category = article.find('category').text

        date_obj = article.find('pubDate').text[5:-6]
        formatted_date_str = datetime.strptime(date_obj, '%d %b %Y %H:%M:%S')
        article_date_time = formatted_date_str.strftime('%Y-%m-%d %H:%M:%S')

        news_dict[article_id] = {
            'article_title': article_title,
            'article_date_time': article_date_time,
            'article_desc': article_desc,
            'article_url': article_url,
            'article_img_url': article_img_url,
            'article_category': article_category,
        }

    return news_dict


# Функция создания JSON-файла с новостями
def create_json_file(news_dict):
    with open('news_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


# Функция добавления новой новости в JSON-файл
def update_json(news_dict):
    with open('news_dict.json', 'r', encoding='UTF-8') as file:
        news_dict_old = json.load(file)

    # Обновление существующих данных новыми данными
    for id_news, decs_news in news_dict.items():
        if id_news in news_dict_old:
            continue
        else:
            article_id = id_news
            article_title = decs_news['article_title']
            article_date_time = decs_news['article_date_time']
            article_desc = decs_news['article_desc']
            article_url = decs_news['article_url']
            article_category = decs_news['article_category']
            article_img_url = decs_news['article_img_url']

            news_dict[article_id] = {
                'article_title': article_title,
                'article_date_time': article_date_time,
                'article_desc': article_desc,
                'article_url': article_url,
                'article_img_url': article_img_url,
                'article_category': article_category,
            }

    # Сохранение обновленных данных обратно в файл
    with open('news_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return news_dict


# Функция создания подключения к базе данных
def create_db_connection():
    try:
        connection = psycopg2.connect(
            user=user,
            host=host,
            password=password,
            database=db_name
        )
        return connection
    except Exception as error:
        print("Ошибка при подключении к PostgreSQL", error)
        return None


# Функция сохранения данных в базу PostgreSQL
def save_data_in_db(connection, news_dict):
    try:
        with connection.cursor() as cursor:
            connection.autocommit = True

            insert_st = '''INSERT INTO news_cs2(id_news, title, date_time, desc_news, url, img_url, category)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id_news) DO NOTHING;'''
            values = []

            for id_news, new_dict in news_dict.items():
                if str.isdigit(id_news):
                    values.append(
                        (id_news, new_dict['article_title'], new_dict['article_date_time'], new_dict['article_desc'],
                         new_dict['article_url'], new_dict['article_img_url'], new_dict['article_category']))

            cursor.executemany(insert_st, values)

    except Exception as error:
        print('Ошибка при сохранении данных в PostgreSQL', error)
    finally:
        connection.close()
        print('Соединение с PostgreSQL закрыто')


def job():
    news_dict = load_articles_from_site()
    connection = create_db_connection()

    if connection:
        save_data_in_db(connection, news_dict)

    # Проверка существует ли JSON-файл
    if os.path.exists('news_dict.json'):
        update_json(news_dict)
    else:
        create_json_file(news_dict)


def main():
    schedule.every(60).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
