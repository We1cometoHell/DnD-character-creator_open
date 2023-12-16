import asyncio

from aiogram import Dispatcher, Bot
from config_data.config import load_config, Config
from handlers import user_handlers


async def main() -> None:
    """Функция конфигурирования и запуска бота"""

    # Выгрузка конфига
    config: Config = load_config()

    # Инициализаторы бота и диспетчера
    bot = Bot(config.tg_bot.bot_token)
    dp = Dispatcher()

    # Здесь мы регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
