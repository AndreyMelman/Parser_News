import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class GismeteoParse:

    def __init__(self):
        self.url = 'https://www.gismeteo.by/news/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/127.0.0.0 Safari/537.36'
        }

    # Функция парсинга новостного сайта
    async def load_articles_from_gismeteo(self):
        # Получаем URL нашего сайта
        response = requests.get(self.url, headers=self.headers)
        # Получаем HTML-файл
        soup = BeautifulSoup(response.content, 'lxml')
        # Получаем кусок HTML-файла с которого будем парсить новости
        articles_items = soup.find_all('div', class_='card-wrap')

        # Создаем словарь для записи новостей
        news_dict = {}

        for article in articles_items:
            article_title = article.find('div', class_='text-title').text
            article_url = f'https://www.gismeteo.by' + article.find('a').get('href')
            article_d = article.find('div', class_='text-excerpt')
            if article_d:
                article_desc = article_d.text
            else:
                article_desc = ''
            article_img_url = article.find('div', class_='img-bg').get('data-src')
            article_category = 'Gismeteo news'
            date_obj = article.find('a').get('data-pub-date')
            article_date = datetime.strptime(date_obj, '%Y-%m-%dT%H:%M:%S')
            article_date_time1 = article_date + timedelta(hours=0)
            article_date_time = article_date_time1.strftime('%Y-%m-%d %H:%M:%S')
            article_id = str(int(article_date.timestamp()))

            news_dict[article_id] = {
                'article_title': article_title,
                'article_date_time': article_date_time,
                'article_desc': article_desc,
                'article_url': article_url,
                'article_img_url': article_img_url,
                'article_category': article_category,
            }

        return news_dict
