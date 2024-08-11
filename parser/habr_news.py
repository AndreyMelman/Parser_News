import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta


# Функция парсинга новостного сайта
def load_articles_from_habr():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/127.0.0.0 Safari/537.36'
    }
    url = 'https://habr.com/ru/news/'
    # Получаем URL нашего сайта
    response = requests.get(url, headers=headers)
    # Получаем HTML-файл
    soup = BeautifulSoup(response.content, 'lxml')
    # Получаем кусок HTML-файла с которого будем парсить новости
    articles_items = soup.find_all('article', class_='tm-articles-list__item')

    # Создаем словарь для записи новостей
    news_dict = {}

    for article in articles_items:
        article_title = article.find_next('a', class_='tm-title__link').text
        article_url = f'https://habr.com' + article.find('a', class_='tm-title__link').get('href')
        article_id = article.get('id')
        article_desc_element = article.find('div',
                                            class_='article-formatted-body article-formatted-body '
                                                   'article-formatted-body_version-2')
        if article_desc_element:
            article_desc = article_desc_element.text
        else:
            article_desc = ''
        article_img = article.find('img', class_='tm-article-snippet__lead-image')
        if article_img and 'src' in article_img.attrs:
            article_img_url = article_img['src']
        else:
            article_img_url = None
        article_category = 'Habr news'
        date_obj = article.find('time').get('datetime')
        article_date = datetime.strptime(date_obj, '%Y-%m-%dT%H:%M:%S.%fZ')
        article_date_time1 = article_date + timedelta(hours=3)
        article_date_time = article_date_time1.strftime('%Y-%m-%d %H:%M:%S')
        news_dict[article_id] = {
            'article_title': article_title,
            'article_date_time': article_date_time,
            'article_desc': article_desc,
            'article_url': article_url,
            'article_img_url': article_img_url,
            'article_category': article_category,
        }

    return news_dict
