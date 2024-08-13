import requests
from bs4 import BeautifulSoup
from datetime import datetime


class DddnewsNewsParser:

    def __init__(self):
        self.url = 'https://3dnews.ru/software-news/rss'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/127.0.0.0 Safari/537.36'
        }

    # Функция парсинга новостного сайта
    async def load_articles_from_3dnews(self):
        # Получаем URL нашего сайта
        response = requests.get(self.url, headers=self.headers)
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
            article_img_url1 = article.find('enclosure')
            if article_img_url1:
                article_img_url = article_img_url1.get('')
            else:
                article_img_url = ''
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
