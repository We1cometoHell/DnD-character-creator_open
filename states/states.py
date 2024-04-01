"""Модуль с классами, отражающими возможные состояния пользователя, в процессе взаимодействия с ботом."""

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


# Cоздаем класс StatesGroup для нашей машины состояний
class FSMCreateCharacter(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    choice_class = State()  # Состояние выбора класса
    choice_race = State()  # Состояние выбора рассы
    choice_backgrounds = State()  # Состояние выбора предыстории
