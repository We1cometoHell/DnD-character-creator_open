"""Вспомогательные функции/методы, помогающие формировать клавиатуры."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция для формирования инлайн-клавиатуры на лету
async def create_inline_kb(
        width: int,
        *args: str,
        start: int = 0,
        exp_callback: str = '',
        last_btn: str | None = None,
        **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args[start:]:
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=f'{exp_callback} {button}' if exp_callback else button)
            )
    if kwargs:
        for key, value in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=f'{key} {value}',
                callback_data=key)
            )

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data=last_btn
        ))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
