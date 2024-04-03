"""Модуль с кастомными фильтрами для хендлеров"""

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class DataInCollection(BaseFilter):
    def __init__(self, method, data):
        self.method = method
        self.data = data

    async def __call__(self, callback: CallbackQuery) -> None | dict:
        collection: dict | None = await self.method()
        return collection[callback.data].get(self.data)
