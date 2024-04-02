"""
Модуль с ORM-моделями базы данных, то есть отображением базы данных в виде объекта с атрибутами, часто совпадающими с
полями базы данных. Через такие объекты можно обращаться к базе данных и как-то взаимодействовать с ней, обращаясь к
атрибутам и методам объектов.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from dataclasses import dataclass
from config_data.config import load_config

config = load_config()

cluster = AsyncIOMotorClient(config.db.db_host.replace('<password>', config.db.db_password))

db = cluster.DnD_character_creator


class DataKeyboard:
    @staticmethod
    async def get_data_keyboard():
        data_keyboard = await db.keyboard_ru.find_one({'_id': 'keyboard'})
        return data_keyboard


class DataClasses:
    @staticmethod
    async def get_data_classes():
        data_classes = await db.classes_ru.find_one({'_id': 'classes'})
        return data_classes


@dataclass
class ManagerUsers:
    _id: int

    async def get_user(self):
        data_users = await db.users.find_one({'_id': self._id})
        return data_users

    async def append_user(self):
        await db.users.insert_one({'_id': self._id})


class StaticData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __setattr__(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = value

    async def load_data(self):
        self.classes = await DataClasses().get_data_classes()
        self.keyboard = await DataKeyboard().get_data_keyboard()
