from aiogram import Bot, Dispatcher
from config_reader import config

tg_bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
telegram_group_id = config.telegram_group_id.get_secret_value()


# Основная функция запуска бота
async def start_bot():
    await tg_bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(tg_bot)
