"""Модуль с хэндлерами для пользователей с обычным статусом, например, для тех, кто первый раз запустил бота."""

from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, Command, CommandStart
from aiogram.types import ChatMemberUpdated, Message
from lexicon.lexicon_ru import LEXICON_RU

# Инициализируем роутер уровня модуля. Фактически, это наследник диспетчера(корневого роутера)
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на блокировку бота пользователем, пока что в таком виде
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f'Пользователь {event.from_user.id} заблокировал бота')
