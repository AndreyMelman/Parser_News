import asyncio
from task.bot import bot
from task.collector import collector
import logging
from task.spammer import spammer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# Основной цикл работы
async def main():
    # Запускаем планировщик задач
    task1 = asyncio.create_task(collector())
    # Запускаем бота
    task2 = asyncio.create_task(bot())
    #
    task3 = asyncio.create_task(spammer())

    await asyncio.gather(task1, task2, task3)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(f'Выход из бота')
