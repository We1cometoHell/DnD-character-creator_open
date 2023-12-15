"""Файл с конфигурационными данными для бота, базы данных, сторонних сервисов и т.п."""

from dataclasses import dataclass
from environs import Env


@dataclass
class DataBaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TelegramBot:
    bot_token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TelegramBot
    db: DataBaseConfig

    def show_config_data(self) -> None:
        """Выводит значения полей экземпляра класса Config на печать,
        чтобы убедиться, что все данные, получаемые из переменных окружения, доступны"""
        print(f'BOT_TOKEN: {self.tg_bot.bot_token}\n'
              f'ADMIN_IDS: {self.tg_bot.admin_ids}\n\n'
              f'DATABASE: {self.db.database}\n'
              f'DB_HOST: {self.db.db_host}\n'
              f'DB_USER {self.db.db_user}\n'
              f'DB_PASSWORD: {self.db.db_password}')


def load_config(path: str | None = None) -> Config:
    # Создаем экземпляр класса Env
    env: Env = Env()
    # Добавляем в переменные окружения данные, прочитанные из файла .env
    env.read_env(path)
    return Config(
        tg_bot=TelegramBot(
            bot_token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DataBaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        )
    )
