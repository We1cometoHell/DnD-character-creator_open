"""Модуль с хэндлерами для пользователей с обычным статусом, например, для тех, кто первый раз запустил бота."""

import asyncio

from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, Command, CommandStart, StateFilter
from aiogram.types import ChatMemberUpdated, Message

from lexicon.lexicon_ru import LEXICON_RU
from models.methods import StaticData
from keyboards.keyboard_utils import create_inline_kb

# Инициализируем роутер уровня модуля. Фактически, это наследник диспетчера(корневого роутера)
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands='create_character'))
async def process_create_hero_command(message: Message):

    # Создаем singleton экземпляр класса StaticData
    db = StaticData()

    # Создаем атрибуты для сохранение данных из БД - быстрый доступ без задержек
    await db.load_data()

    # Получаем список классов из БД для формирования клавиатуры
    buttons = list(db.classes.keys())[1:]

    # Задаем параметры для inline keyboard
    keyboard = create_inline_kb(buttons, 3)

    # Нужно сделать текст по середине панели + добавить картинку
    await message.answer(text='Каким классом вы хотите играть?', reply_markup=keyboard)


# @router.message(F.text.lower().in_(['character_classes']))
# async def process_selection_class(message: Message):
#     await message.answer(text='Отлично идем дальше')


@router.message()
async def process_answer_any(message: Message):
    await message.answer(text='Я тебя не понимаю')


# Этот хэндлер будет срабатывать на блокировку бота пользователем, пока что в таком виде
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f'Пользователь {event.from_user.id} заблокировал бота')
