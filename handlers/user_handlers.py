"""Модуль с хэндлерами для пользователей с обычным статусом, например, для тех, кто первый раз запустил бота."""

from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, Command, CommandStart, StateFilter
from aiogram.types import ChatMemberUpdated, Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import lexicon_ru
from models.models import kb_loader, manager_users
from keyboards.keyboard_utils import create_inline_kb
from states.states import FSMCreateCharacter
from filters.custom_filters import DataInCollection
from utils.utils import stats_calculator

# Инициализируем роутер уровня модуля. Фактически, это наследник диспетчера(корневого роутера)
router = Router()


# Хендлер команды /start в дефолтном состоянии
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    _id = message.chat.id
    if not await manager_users.get_user(_id):
        await manager_users.append_user(_id)
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
async def process_create_character_command(message: Message, state: FSMContext):
    # Получаем данные о классах
    classes: dict = await kb_loader.get_data_classes()

    # Задаем параметры для inline keyboard
    keyboard = await create_inline_kb(3, *classes, start=1)

    # Нужно сделать текст по середине панели + добавить картинку + добавить текст отклик на нажатие
    await message.answer(text=lexicon_ru.LEXICON_RU_DEF_STATE['/create_character'],
                         reply_markup=keyboard)
    # Устанавливаем состояние выбора класса
    await state.set_state(FSMCreateCharacter.choice_class)


# Хендлер выбора рассы, после выбора класса
@router.callback_query(StateFilter(FSMCreateCharacter.choice_class))
async def process_class_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о классе (callback.data нажатой кнопки) в хранилище
    await state.update_data(_class=callback.data)
    await callback.message.delete()

    # Получаем данные о рассах
    races: dict = await kb_loader.get_data_races()

    # Задаем параметры для inline keyboard
    keyboard = await create_inline_kb(3, *races, start=1)
    await callback.message.answer(text=lexicon_ru.LEXICON_RU_NDEF_STATE['choice_race'],
                                  reply_markup=keyboard)
    # Устанавливаем состояние ожидания выбора рассы
    await state.set_state(FSMCreateCharacter.choice_race)


# Хендлер выбора подрассы, после выбора рассы
@router.callback_query(
    StateFilter(FSMCreateCharacter.choice_race),
    DataInCollection(kb_loader.get_data_races, 'variety'))
async def process_race_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о рассе (callback.data нажатой кнопки) в хранилище
    await state.update_data(race=callback.data)
    await callback.message.delete()

    # Получаем данные о рассах
    races: dict = await kb_loader.get_data_races()

    # Получаем список подрасс из загруженных данных для формирования клавиатуры
    buttons = races[callback.data]['variety']

    # Задаем параметры для inline keyboard
    keyboard = await create_inline_kb(3, *buttons)
    await callback.message.answer(text=lexicon_ru.LEXICON_RU_NDEF_STATE['choice_variety'],
                                  reply_markup=keyboard)
    # Устанавливаем состояние ожидания выбора рассы
    await state.set_state(FSMCreateCharacter.choice_variety)


# Хендлер выбора метода определения значений характеристик, после выбора рассы
@router.callback_query(StateFilter(FSMCreateCharacter.choice_race))
async def process_race_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о рассе (callback.data нажатой кнопки) в хранилище
    await state.update_data(race=callback.data)
    await callback.message.delete()

    # Получаем список ответов из lexicon_ru для формирования клавиатуры
    buttons = lexicon_ru.LEXICON_RU_VARIANTS['choice_stats_method']

    # Задаем параметры для inline keyboard
    keyboard = await create_inline_kb(2, *buttons)
    await callback.message.answer(
        text=lexicon_ru.LEXICON_RU_NDEF_STATE['choice_stats_method'],
        reply_markup=keyboard
    )
    # Устанавливаем состояние ожидания выбора характеристик
    await state.set_state(FSMCreateCharacter.choice_stats_method)


# Хендлер выбора метода определения значений характеристик, после выбора подрассы
@router.callback_query(StateFilter(FSMCreateCharacter.choice_variety))
async def process_stats_method_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о подрассе (callback.data нажатой кнопки) в хранилище
    await state.update_data(variety=callback.data)
    await callback.message.delete()

    # Получаем список ответов из lexicon_ru для формирования клавиатуры
    buttons = lexicon_ru.LEXICON_RU_VARIANTS['choice_stats_method']

    # Задаем параметры для inline keyboard
    keyboard = await create_inline_kb(1, *buttons)
    await callback.message.answer(
        text=lexicon_ru.LEXICON_RU_NDEF_STATE['choice_stats_method'],
        reply_markup=keyboard
    )
    # Устанавливаем состояние ожидания выбора характеристик
    await state.set_state(FSMCreateCharacter.choice_stats_method)


# Хендлер выбора характеристик, после выбора калькулятора характеристик
@router.callback_query(StateFilter(
    FSMCreateCharacter.choice_stats_method),
    F.data == lexicon_ru.LEXICON_RU_VARIANTS['choice_stats_method'][2]
)
async def process_calc_stats_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о характеристиках в хранилище
    await state.update_data(
        stats=stats_calculator.stats,
        count_stats=stats_calculator.count_stats
    )
    await callback.message.delete()

    # Получаем список ответов из экземпляра класса StatsCalculator для формирования клавиатуры
    buttons = stats_calculator.stats
    # Получаем количество оставшихся очков для покупки характеристик
    count_stats = stats_calculator.count_stats

    # Задаем параметры для inline keyboard
    keyboard = await create_inline_kb(2, **buttons,
                                      last_btn=lexicon_ru.LEXICON_RU_NDEF_STATE['end_choice_stats'])

    await callback.message.answer(
        text=lexicon_ru.LEXICON_RU_NDEF_STATE['choice_stats'].format(count_stats),
        reply_markup=keyboard
    )

    # Устанавливаем состояние ожидания выбора характеристики
    await state.set_state(FSMCreateCharacter.choice_calc_stats)


# Хендлер выбора значения характеристики, после выбора выбора характеристики
@router.callback_query(StateFilter(FSMCreateCharacter.choice_calc_stats))
async def process_stat_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о характеристике (callback.data нажатой кнопки) в переменную
    stat = callback.data

    await callback.message.delete()

    # Получаем данные пользователя из БД
    data = await state.get_data()
    # Сохраняем текущее количество очков и значение
    # выбранной характеристики в переменные
    count_stats = data['count_stats']
    stat_v = data['stats'][stat]

    # Получаем список ответов из экземпляра класса StatsCalculator для формирования клавиатуры
    buttons = await stats_calculator.get_possible_stats(count_stats, stat_v)

    # Задаем параметры для inline keyboard
    keyboard = await create_inline_kb(4, *buttons, exp_callback=stat)
    await callback.message.answer(
        text=lexicon_ru.LEXICON_RU_NDEF_STATE['choice_stat'].format(stat),
        reply_markup=keyboard
    )

    await state.set_state(FSMCreateCharacter.choice_stat)


@router.callback_query(StateFilter(FSMCreateCharacter.choice_stat))
async def process_calc_stats_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем новые данные о характеристике (название, значение)
    # (callback.data нажатой кнопки) в переменные
    k_stat, new_v_stat = callback.data.split()
    await callback.message.delete()

    # Получаем данные пользователя из БД
    data = await state.get_data()
    # Словарь характеристик и значений
    stats = data['stats']
    # Старое значение счетчика
    old_count_stats = data['count_stats']
    # Старое значение характеристики
    old_v_stat = stats[k_stat]
    # Меняем значение характеристики на новое и обновляем счетчик
    v_stat, count_stats = await stats_calculator.change_stat(
        int(new_v_stat), old_v_stat, old_count_stats
    )
    # Устанавливаем новое значение в словарь
    stats[k_stat] = v_stat

    # Обновляем данные пользователя
    await state.update_data(stats=stats, count_stats=count_stats)

    # Задаем параметры для inline keyboard
    keyboard = await create_inline_kb(2, **stats,
                                      last_btn=lexicon_ru.LEXICON_RU_NDEF_STATE['end_choice_stats'])
    await callback.message.answer(
        text=lexicon_ru.LEXICON_RU_NDEF_STATE['choice_stats'].format(count_stats),
        reply_markup=keyboard
    )

    # Устанавливаем состояние ожидания выбора характеристики
    await state.set_state(FSMCreateCharacter.choice_calc_stats)


# @router.callback_query(StateFilter(FSMCreateCharacter))


# Хендлер отвечающий на любой отправленный апдейт от пользователя
# кроме нужного callback в любом состоянии != дефолтному
@router.message(~StateFilter(default_state))
async def process_wrong_answer(message: Message, state: FSMContext):
    name_state = await state.get_state()
    await message.answer(text=lexicon_ru.LEXICON_RU_F_ANSWERS[name_state])


# Хендлер отвечающий на любой отправленный апдейт от пользователя
# в состоянии по умолчанию, кроме тех для которых есть
# отдельные хэндлеры
@router.message(StateFilter(default_state))
async def process_answer_any(message: Message):
    await message.answer(text=lexicon_ru.LEXICON_RU_DEF_STATE['answer_any'])


# Этот хэндлер будет срабатывать на блокировку бота пользователем, пока что в таком виде
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f'Пользователь {event.from_user.id} заблокировал бота')
