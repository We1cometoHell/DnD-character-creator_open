"""Модуль с хэндлерами для пользователей с обычным статусом, например, для тех, кто первый раз запустил бота."""

from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, Command, CommandStart, StateFilter
from aiogram.types import ChatMemberUpdated, Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import lexicon_ru
from models.models import StaticData, DataUsers
from keyboards.keyboard_utils import create_inline_kb
from states.states import FSMCreateCharacter

# Инициализируем роутер уровня модуля. Фактически, это наследник диспетчера(корневого роутера)
router = Router()


# Хендлер команды /start в дефолтном состоянии
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    user_data = DataUsers(_id=message.chat.id)
    if not await user_data.get_data_user():
        await user_data.append_user()
    await message.answer(text=lexicon_ru.LEXICON_RU_DEF_STATE['/start'])


# Хендлер команды /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=lexicon_ru.LEXICON_RU_NDEF_STATE['/help'])


# Хендлер команды /cancel в дефолтном состоянии
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=lexicon_ru.LEXICON_RU_DEF_STATE['/cancel'])


# Хендлер команды /cancel в любых состояних, кроме
# состояния по умолчанию. Переводит машину состояний дефолт
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=lexicon_ru.LEXICON_RU_NDEF_STATE['/cancel'])

    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Хендлер команды /create_character в дефолтном состоянии
@router.message(Command(commands='create_character'), StateFilter(default_state))
async def process_create_hero_command(message: Message, state: FSMContext):
    # Создаем singleton экземпляр класса StaticData
    db = StaticData()

    # Создаем атрибуты для сохранение данных из БД - быстрый доступ без задержек
    await db.load_data()

    # Получаем список классов из БД для формирования клавиатуры
    buttons = list(db.classes.keys())[1:]

    # Задаем параметры для inline keyboard
    keyboard = create_inline_kb(buttons, 3)

    # Нужно сделать текст по середине панели + добавить картинку + добавить текст отклик на нажатие
    await message.answer(text=lexicon_ru.LEXICON_RU_DEF_STATE['/create_character'],
                         reply_markup=keyboard)
    # Устанавливаем состояние выбора класса
    await state.set_state(FSMCreateCharacter.choice_class)


# Этот хэндлер будет срабатывать, если во время выбора класса
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMCreateCharacter.choice_class))
async def warning_not_class(message: Message):
    await message.answer(text=lexicon_ru.LEXICON_RU_F_ANSWERS['/create_character'])


@router.callback_query(StateFilter(FSMCreateCharacter.choice_class))
async def process_class_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем класс (callback.data нажатой кнопки) в хранилище,
    # по ключу "_class", для получения словаря используй
    # await state.get_data()
    await state.update_data(_class=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        text='Отлично идем дальше'
    )
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMCreateCharacter.choice_race)


# Хендлер отвечающий на любой отправленный апдейт от пользователя,
# кроме тех для которых есть отдельные хэндлеры, вне состояний
@router.message()
async def process_answer_any(message: Message):
    await message.answer(text='Я тебя не понимаю')


# Этот хэндлер будет срабатывать на блокировку бота пользователем, пока что в таком виде
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f'Пользователь {event.from_user.id} заблокировал бота')
