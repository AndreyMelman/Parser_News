from config_reader import user, host, password, db_name
import psycopg2


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


# Функция получения новых новостей из базы PostgreSQL
def get_news_from_db(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT id_news, title, date_time, desc_news, url, img_url, category
                              FROM news_cs2
                              WHERE sent_to_telegram = FALSE
                              ORDER BY date_time DESC''')
            news = cursor.fetchall()

            return news

    except Exception as error:
        print('Ошибка при получении данных из PostgreSQL', error)
        return []


# Функция обновления столбца sent_to_telegram, для отправления в телеграм новых новостей
def mark_news_as_sent(connection, news_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE news_cs2 SET sent_to_telegram = TRUE WHERE id_news = %s;', (news_id,))
            connection.commit()
    except Exception as error:
        print(f"Ошибка при обновлении статуса новости: {error}")


def close(connection):
    if connection:
        connection.close()
        print('Соединение с PostgreSQL закрыто')
