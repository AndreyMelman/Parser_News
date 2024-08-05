import asyncio
from telegram_bot import start_bot, parse_and_send_news


# Планировщик задач
async def schedule_task():
    while True:
        await parse_and_send_news()
        await asyncio.sleep(3600)  # Запускать каждые 60 минут


# Основной цикл работы
async def main():
    # Запускаем планировщик задач
    task1 = asyncio.create_task(schedule_task())
    # Запускаем бота
    task2 = asyncio.create_task(start_bot())

    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
