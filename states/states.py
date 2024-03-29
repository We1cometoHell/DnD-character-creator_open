"""Модуль с классами, отражающими возможные состояния пользователя, в процессе взаимодействия с ботом."""

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

