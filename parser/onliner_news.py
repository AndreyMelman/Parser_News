import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Функция парсинга новостного сайта
def load_articles_from_onliner():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/127.0.0.0 Safari/537.36'
    }
    url = 'https://tech.onliner.by/'
    # Получаем URL нашего сайта
    response = requests.get(url, headers=headers)
    # Получаем HTML-файл
    soup = BeautifulSoup(response.content, 'lxml')
    # Получаем кусок HTML-файла с которого будем парсить новости
    articles_items = soup.find_all('div', class_='news-tidings__item_condensed')

    # Создаем словарь для записи новостей
    news_dict = {}

    for article in articles_items:
        article_title = article.find('a', class_='news-tidings__link').find_next('span').text
        article_url = f'https://tech.onliner.by' + article.find('a', class_='news-tidings__stub').get('href')
        article_id = article.get('data-post-date')
        article_desc = article.find('div', class_='news-helpers_hide_mobile-small').text.strip()
        article_img_url = article.find('img').get('src')
        article_category = 'tech.onliner'
        article_date_time_unix = article.get('data-post-date')
        article_date_time = datetime.fromtimestamp(int(article_date_time_unix))

        news_dict[article_id] = {
            'article_title': article_title,
            'article_date_time': article_date_time,
            'article_desc': article_desc,
            'article_url': article_url,
            'article_img_url': article_img_url,
            'article_category': article_category,
        }

    return news_dict
