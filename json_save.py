import json


# Функция создания JSON-файла с новостями
def create_json_file(news_dict):
    with open('news_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


# Функция добавления новой новости в JSON-файл
def update_json(news_dict):
    with open('news_dict.json', 'r', encoding='UTF-8') as file:
        news_dict_old = json.load(file)

    # Обновление существующих данных новыми данными
    for id_news, decs_news in news_dict.items():
        if id_news in news_dict_old:
            continue
        else:
            article_id = id_news
            article_title = decs_news['article_title']
            article_date_time = decs_news['article_date_time']
            article_desc = decs_news['article_desc']
            article_url = decs_news['article_url']
            article_category = decs_news['article_category']
            article_img_url = decs_news['article_img_url']

            news_dict[article_id] = {
                'article_title': article_title,
                'article_date_time': article_date_time,
                'article_desc': article_desc,
                'article_url': article_url,
                'article_img_url': article_img_url,
                'article_category': article_category,
            }

    # Сохранение обновленных данных обратно в файл
    with open('news_dict.json', 'w', encoding='UTF-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return news_dict
