import asyncio
import logging

from aiogram import Dispatcher, Bot

from config_data.config import load_config, Config
from handlers import user_handlers
from keyboards.set_menu import set_main_menu
from states.states import MongoMemoryStorage

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}] #{levelname:8} {filename}:'
               '{lineno} - {name} - {message}',
        style='{'
    )

    # Выгрузка конфига
    config: Config = load_config()

    # Хранилище состояний
    storage = MongoMemoryStorage()

    # Инициализаторы бота и диспетчера
    bot = Bot(config.tg_bot.bot_token)
    dp = Dispatcher(storage=storage)

    # Устанавливает кнопку Menu
    await set_main_menu(bot)

    # Здесь мы регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
