from aiogram import Bot, Dispatcher
from config_reader import config
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from task import used_bot

bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
telegram_group_id = config.telegram_group_id.get_secret_value()


# Основная функция запуска бота
async def start_bot():
    dp.include_router(used_bot.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
