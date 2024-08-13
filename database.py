import logging

import psycopg2
from config_reader import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# Класс для управления подключением к базе данных
class DatabaseConnection:

    def __init__(self, user=config.db_user.get_secret_value(),
                 host=config.db_host.get_secret_value(),
                 password=config.db_password.get_secret_value(),
                 database=config.db_name.get_secret_value()):
        self.__user = user
        self.__host = host
        self.__password = password
        self.__database = database
        self.connection = None

    # Функция создания подключения к базе данных
    def create_db_connection(self):
        try:
            self.connection = psycopg2.connect(
                user=self.__user,
                host=self.__host,
                password=self.__password,
                database=self.__database
            )
            logging.info(f'Успешное подключение к базе данных')
            return self.connection
        except Exception as error:
            logging.error(f'Ошибка при подключении к PostgreSQL: {error}')
            return None

    def close_db(self):
        if self.connection:
            self.connection.close()
            logging.info(f'Соединение с PostgreSQL закрыто')


# Класс для выполнения операций с базой данных
class NewsRepository:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    # Функция сохранения данных в базу PostgreSQL
    async def save_data_in_db(self, news_dict):
        connection = self.db_connection.connection
        if not connection:
            logging.error(f'Нет активного подключения к базе данных')
        try:
            with connection.cursor() as cursor:

                insert_st = '''INSERT INTO news_cs2(id_news, title, date_time, desc_news, url, img_url, category)
                            VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id_news) DO NOTHING;'''
                values = []

                for id_news, new_dict in news_dict.items():
                    if str.isdigit(id_news):
                        values.append(
                            (
                                id_news, new_dict['article_title'], new_dict['article_date_time'],
                                new_dict['article_desc'],
                                new_dict['article_url'], new_dict['article_img_url'], new_dict['article_category']))

                cursor.executemany(insert_st, values)

                connection.commit()

        except Exception as error:
            logging.error(f'Ошибка при сохранении данных в PostgreSQL: {error}')

    # Функция получения новых новостей из базы PostgreSQL
    async def get_unread_news(self):
        connection = self.db_connection.connection
        if not connection:
            logging.error(f'Нет активного подключения к базе данных')
        try:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT id_news, title, date_time, desc_news, url, img_url, category
                                      FROM news_cs2
                                      WHERE sent_to_telegram = FALSE
                                      ORDER BY date_time DESC''')
                news = cursor.fetchall()

                return news

        except Exception as error:
            logging.error(f'Ошибка при получении данных из PostgreSQL: {error}')
            return []

    # Функция обновления столбца sent_to_telegram, для отправления в телеграм новых новостей
    async def mark_news_as_sent(self, list_id):
        connection = self.db_connection.connection
        if not connection:
            logging.error(f'Нет активного подключения к базе данных')
        list_id = tuple(list_id)
        try:
            with connection.cursor() as cursor:
                cursor.execute('UPDATE news_cs2 SET sent_to_telegram = TRUE WHERE id_news IN %s;', (list_id,))
                connection.commit()
        except Exception as error:
            logging.error(f'Ошибка при обновлении статуса новости: {error}')
