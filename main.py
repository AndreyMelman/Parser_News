import json
import requests
from bs4 import BeautifulSoup
import psycopg2
from config import host, user, password, db_name


# Функция получения новостей в JSON-файл
def get_first_news():
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

    with open('news_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


# Получение новых новостей с сохранением в JSON-файл
def check_news_update():
    with open('news_dict.json', 'r', encoding='UTF-8') as file:
        news_dict = json.load(file)

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
    fresh_news = {}

    for article in articles_cards:
        article_url = f'https://3dnews.ru/{article.find('a').get('href')}'
        article_id = article_url.split('/')[-2]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find('a', class_='entry-header').text.strip()
            article_desc = article.find('p').text.strip()
            article_date_time = article.find('span', class_='entry-date').text.strip()

        # Занесение новых новостей в базу данных
        connection = None
        try:
            connection = psycopg2.connect(
                user=user,
                host=host,
                password=password,
                database=db_name
            )
            connection.autocommit = True
            # Добавим данные в таблицу News

            with connection.cursor() as cursor:
                sql_query = 'INSERT INTO news(news_id, title, decs, url) VALUES (%s, %s, %s, %s);'
                values = (article_id, article_title, article_desc, article_url)
                cursor.execute(sql_query, values)

        except Exception as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")

        news_dict[article_id] = {
            'article_date_time': article_date_time,
            'article_title': article_title,
            'article_desc': article_desc,
            'article_url': article_url,
        }

        fresh_news[article_id] = {
            'article_date_time': article_date_time,
            'article_title': article_title,
            'article_desc': article_desc,
            'article_url': article_url,
        }
    with open('news_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    # get_first_news()
    print(check_news_update())


if __name__ == '__main__':
    main()
