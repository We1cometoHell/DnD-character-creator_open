"""Модуль с кастомными фильтрами для хендлеров"""

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class DataInCollection(BaseFilter):
    def __init__(self, method, data):
        self.method = method
        self.data = data

    async def __call__(self, callback: CallbackQuery) -> None | dict:
        collection: dict | None = await self.method()
        key: str = callback.data

        for k in self.data:
            collection = collection[key].get(k)
            if collection:
                key = k
            else:
                break

        return collection
