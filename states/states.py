"""Модуль с классами, отражающими возможные состояния пользователя, в процессе взаимодействия с ботом."""

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import BaseStorage, StorageKey
from typing import Any

from models.models import db


# Cоздаем класс StatesGroup для нашей машины состояний
class FSMCreateCharacter(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    choice_class = State()  # Состояние выбора класса
    choice_race = State()  # Состояние выбора рассы
    choice_backgrounds = State()  # Состояние выбора предыстории


# Реализация MemoryStorage для MongoDB
class MongoMemoryStorage(BaseStorage):
    @staticmethod
    async def get_data_user(_id):
        return await db.users.find_one({'_id': _id})

    async def set_state(self, key: StorageKey, state: str | State | None = None) -> None:
        """
        Функция устанавливающая состояние заполнения листа в БД.

        :param key: принимает экземпляр StorageKey хранящий id: пользователя, бота, чата.
        :param state: принимает текущее состояние машины - FSM.
        """
        state_name: str = state.state if isinstance(state, State) else state
        await db.users.update_one(
            {'_id': key.user_id},
            {'$set': {'state': state_name}},
            upsert=True
        )

    async def get_state(self, key: StorageKey) -> str | None:
        user_data: dict | None = await self.get_data_user(key.user_id)
        if user_data:
            return user_data.get('state')
        return

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        """
        Write data (replace)

        :param key: storage key
        :param data: new data
        """
        await db.users.update_one(
            {'_id': key.user_id},
            {'$set': {'sheet_data': data}}
        )

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        """
        Get current data for key

        :param key: storage key
        :return: current data
        """
        user_data: dict | None = await self.get_data_user(key.user_id)
        if user_data:
            return user_data.get('sheet_data')
        return {}

    async def update_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        """
        Update date in the storage for key (like dict.update)

        :param key: storage key
        :param data: partial data
        :return: new data
        """
        for k, v in data.items():
            await db.users.update_one(
                {'_id': key.user_id},
                {'$set': {f'sheet_data.{k}': v}},
                upsert=True
            )

    async def close(self) -> None:  # pragma: no cover
        """
        Close storage (database connection, file or etc.)

        !!! ДОПИСАТЬ !!!

        """
        pass
