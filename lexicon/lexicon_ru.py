"""Модуль со словарем соответствий данных текстам на русском языке."""

LEXICON_RU_DEF_STATE: dict[str, str] = {
    '/start': 'Вы запустили бота, пока что автор не добавил нужную информацию',
    '/cancel': 'Вы не заполняете лист персонажа - эта команда не активна\n\n'
               'Чтобы перейти к заполнению - отправьте команду\n/create_character или выберете ее в Menu',
    '/create_character': 'Каким классом вы хотите играть?'
}

LEXICON_RU_NDEF_STATE: dict[str, str] = {
    '/start': 'Я уже запущен, если нужна помощь обратитесь к команде /help',
    '/help': 'Я должен помочь вам в создании персонажа для днд, но мои создатели еще ничего не сделали',
    '/cancel': 'Вы прервали заполнения листа персонажа\n\n'
               'Чтобы начать заново - отправьте команду\n/create_character или выберете ее в Menu',
    '/create_character': 'Вы уже выбрали класс'
}

LEXICON_RU_F_ANSWERS: dict[str, str] = {
    '/create_character': 'Пожалуйста, пользуйтесь кнопками при выборе класса\n\n'
                         'Если вы хотите прервать заполнение анкеты - отправьте команду /cancel '
                         'или выберете ее в Menu'
}

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Запустите бота и познакомьтесь с тем, что он умеет 🚀',
    '/help': 'Получите подробное описание о командах и возможностях 📖',
    '/cancel': 'Сбросить заполнение листа персонажа ❌',
    '/create_character': 'Создайте персонажа для DnD5e ⚔️'
}
