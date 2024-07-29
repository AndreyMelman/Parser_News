import json
import requests
from bs4 import BeautifulSoup
import psycopg2
from config import host, user, password, db_name


# Функция парсинга новостного сайта
def load_articles_from_site():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/127.0.0.0 Safari/537.36'
    }
    url = 'https://3dnews.ru/news/#software'
    # Получаем URL нашего сайта
    response = requests.get(url, headers=headers)
    # Получаем HTML-файл
    soup = BeautifulSoup(response.text, 'lxml')
    # Получаем кусок HTML-файла с которого будем парсить новости
    articles_cards = soup.find_all('div',
                                   class_='article-entry article-infeed marker_sw '
                                          'nImp0 nIcat10 cat_10 nIaft newsAllFeedHideItem')
    # Создаем словарь для записи новостей
    news_dict = {}

    for article in articles_cards:
        article_title = article.find('a', class_='entry-header').text.strip()
        article_desc = article.find('p').text.strip()
        article_url = f'https://3dnews.ru/{article.find('a').get('href')}'
        article_date_time = article.find('span', class_='entry-date').text.strip()

        article_id = article_url.split('/')[-2]

        news_dict[article_id] = {
            'article_date_time': article_date_time,
            'article_title': article_title,
            'article_desc': article_desc,
            'article_url': article_url,
        }

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
    cursor = None
    try:
        cursor = connection.cursor()
        connection.autocommit = True

        for id_news, new_dict in news_dict.items():
            # Проверяем существует ли новость в базе данных
            cursor.execute('SELECT news_id FROM news WHERE news_id = %s', (id_news,))
            result = cursor.fetchone()

            if not result:
                # Добавляем новую новость
                cursor.execute('''
                INSERT INTO news(news_id, title, decs, url, date_time)
                VALUES (%s, %s, %s, %s, %s)''',
                               (id_news, new_dict['article_title'], new_dict['article_desc'], new_dict['article_url'],
                                new_dict['article_date_time']))
    except Exception as error:
        print('Ошибка при сохранении данных в PostgreSQL', error)
    finally:
        connection.close()
        cursor.close()
        print('Соединение с PostgreSQL закрыто')


def main():
    news_dict = load_articles_from_site()
    connection = create_db_connection()

    if connection:
        save_data_in_db(connection, news_dict)


if __name__ == '__main__':
    main()
