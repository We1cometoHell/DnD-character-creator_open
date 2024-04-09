"""
Модуль с ORM-моделями базы данных, то есть отображением базы данных в виде объекта с атрибутами, часто совпадающими с
полями базы данных. Через такие объекты можно обращаться к базе данных и как-то взаимодействовать с ней, обращаясь к
атрибутам и методам объектов.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from config_data.config import load_config

config = load_config()

cluster = AsyncIOMotorClient(config.db.db_host.replace('<password>', config.db.db_password))

db = cluster.DnD_character_creator


class KeyboardLoader:
    @staticmethod
    async def get_data_races() -> dict | None:
        data_keyboard = await db.races_ru.find_one({'_id': 'races'})
        return data_keyboard

    @staticmethod
    async def get_data_classes() -> dict | None:
        data_classes = await db.classes_ru.find_one({'_id': 'classes'})
        return data_classes

    @staticmethod
    async def get_data_backgrounds() -> dict | None:
        data_backgrounds = await db.backgrounds_ru.find_one({'_id': 'backgrounds'})
        return data_backgrounds


class ManagerUsers:
    @staticmethod
    async def get_user(_id) -> dict | None:
        return await db.users.find_one({'_id': _id})

    @staticmethod
    async def append_user(_id) -> None:
        await db.users.insert_one({'_id': _id})


# Создаем экземпляр класса KeyboardLoader
# для получения данных клавиатуры
kb_loader = KeyboardLoader()
# Создаем экземпляр класса ManagerUsers
# для управления данными пользователя
manager_users = ManagerUsers()

# class StaticData:
#     __instance = None
#     __kb_loader = KeyboardLoader()
#
#     def __new__(cls):
#         if cls.__instance is None:
#             cls.__instance = super().__new__(cls)
#         return cls.__instance
#
#     def __setattr__(self, key: str, value: dict):
#         if key not in self.__dict__:
#             self.__dict__[key] = value
