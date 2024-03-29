"""Вспомогательные функции/методы, помогающие формировать клавиатуры."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(buttons: list[str], width: int) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=i, callback_data=i) for i in buttons]

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# class KeyboardClasses:
