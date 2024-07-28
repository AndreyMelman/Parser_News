import json
import requests
from bs4 import BeautifulSoup


# Функция получения новостей в JSON-файл
def get_first_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/127.0.0.0 Safari/537.36'
    }
    url = 'https://3dnews.ru/news/#software'
    # Получаем URL нашего сайта
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    articles_cards = soup.find_all('div',
                                   class_='article-entry article-infeed marker_sw '
                                          'nImp0 nIcat10 cat_10 nIaft newsAllFeedHideItem')

    news_dict = {}

    for article in articles_cards:
        article_title = article.find('a', class_='entry-header').text.strip()
        article_desc = article.find('p').text.strip()
        article_url = f'https://3dnews.ru/{article.find('a').get('href')}'
        article_date_time = article.find('span', class_='entry-date').text.strip()

        article_id = article_url.split('/')[-2]

        # print(f'{article_id} | {article_title} | {article_desc} | {article_url} | {article_date_time}')

        news_dict[article_id] = {
            'article_date_time': article_date_time,
            'article_title': article_title,
            'article_desc': article_desc,
            'article_url': article_url,
        }

    with open('news_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def main():
    get_first_news()


if __name__ == '__main__':
    main()
