from database import create_db_connection, save_data_in_db, get_news_from_db, close
import os
from parser import load_articles_from_site
from json_save import create_json_file, update_json

import schedule
import time


def job():
    news_dict = load_articles_from_site()
    connection = create_db_connection()

    if connection:
        # Сохраняем в базу новые новости
        save_data_in_db(connection, news_dict)

        close(connection)

    # Проверка существует ли JSON-файл
    if os.path.exists('news_dict.json'):
        update_json(news_dict)
    else:
        create_json_file(news_dict)


def main():
    schedule.every(30).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
