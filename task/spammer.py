import asyncio
from task.bot import send_news


# Функция запускает отправку новостей в телеграм бот каждые 2 часа
async def spammer():
    while True:
        await send_news()
        await asyncio.sleep(60*60*2)  # Запускать каждые 120 минут
