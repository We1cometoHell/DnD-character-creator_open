"""Вспомогательные функции/методы, помогающие формировать клавиатуры."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from models.methods import DataKeyboard
import asyncio

data_keyboard = asyncio.run(DataKeyboard().get_data_keyboard)


# class KeyboardClasses:
