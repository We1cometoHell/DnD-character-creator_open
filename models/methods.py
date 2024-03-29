"""Модуль с методами для работы с БД."""
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from dataclasses import dataclass
from config_data.config import load_config

classes = {
    'Бард': {
        'hit-die': 'd8',
        'base_code': 'cha',
        'armor': ('Легкий доспех',),
        'weapons': ('Простое оружие', 'Длинные мечи', 'Короткие мечи', 'Рапира', 'Арбалет, ручной'),
        'tools': {'Музыкальный инструмент': 3},
        'saves': ('dex', 'cha'),
        'skills': {
            'skill': ('Атлетика', 'Акробатика', 'Лoвкость рук', 'Скрытность', 'Магия', 'История', 'Анализ', 'Природа',
                      'Религия', 'Уход за животными', 'Проницательность', 'Медицина', 'Внимательность', 'Выживание',
                      'Обман', 'Запугивание', 'Выступление', 'Убеждение'),
            'count': 3},
        'start_equip': (('Рапира', 'Длинный меч', 'Простое оружие'), ('Набор дипломата', 'Набор артиста'),
                        ('Лютня', 'Музыкальный иснтрумент'), 'Кожанный доспех', 'Кинжал'),
        '1_level': ('Вдохновение барда:\nСвоими словами или музыкой вы можете вдохновлять других. Для этого вы должны '
                    'бонусным действием выбрать одно существо, отличное от вас, в пределах 60 футов, которое может вас '
                    'слышать. Это существо получает кость бардовского вдохновения — к6.В течение следующих 10 минут '
                    'это существо может один раз бросить эту кость и добавить результат к своему броску. Добавлять '
                    'можно к проверке характеристики, атаке или спасброску. Существо может принять решение о броске '
                    'кости вдохновения уже после броска к20, но должно сделать это прежде, чем Мастер объявит '
                    'результат броска. Как только кость бардовского вдохновения брошена, она исчезает. Существо может '
                    'иметь только одну такую кость одновременно.Вы можете использовать это умение количество раз, '
                    'равное модификатору вашей Харизмы, но как минимум один раз. Потраченные использования этого '
                    'умения восстанавливаются после продолжительного отдыха.\nВаша Кость бардовского вдохновения '
                    'изменяется с ростом вашего уровня в этом классе. Она становится к8 на 5 уровне, к10 на 10 уровне '
                    'и к12 на 15 уровне.',)
    },
    'Варвар': {
        'hit-die': 'd12',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Воин': {
        'hit-die': 'd10',
        'armor': ('Легкий доспех', 'Средний доспех', 'Тяжелый доспех', 'Щит')
    },
    'Волшебник': {
        'hit-die': 'd6',
        'base_code': 'int'
    },
    'Друид': {
        'hit-die': 'd8',
        'base_code': 'wis',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Жрец': {
        'hit-die': 'd8',
        'base_code': 'wis',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Изобретатель': {
        'hit-die': 'd8',
        'base_code': 'int',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Колдун': {
        'hit-die': 'd8',
        'base_code': 'cha',
        'armor': ('Легкий доспех',)
    },
    'Монах': {
        'hit-die': 'd8'
    },
    'Паладин': {
        'hit-die': 'd10',
        'base_code': 'cha',
        'armor': ('Легкий доспех', 'Средний доспех', 'Тяжелый доспех', 'Щит')
    },
    'Плут': {
        'hit-die': 'd8',
        'armor': ('Легкий доспех',)
    },
    'Следопыт': {
        'hit-die': 'd10',
        'base_code': 'wis',
        'armor': ('Легкий доспех', 'Средний доспех', 'Щит')
    },
    'Чародей': {
        'hit-die': 'd6',
        'base_code': 'cha'
    },
}

# db.users.insert_one({'_id': 'users'})  # Добавляет документ в коллекцию
# db.classes_ru.update_one({'_id': 'classes'}, {'$set': classes})
# добавляет либо изменяет поле документа в коллекции

config = load_config()

cluster = AsyncIOMotorClient(config.db.db_host.replace('<password>', config.db.db_password))

db = cluster.DnD_character_creator


class DataKeyboard:
    @property
    async def get_data_keyboard(self):
        data_keyboard = await db.keyboard_ru.find_one({'_id': 'keyboard'})
        return data_keyboard


class DataClasses:
    @property
    async def get_data_classes(self):
        data_classes = await db.classes_ru.find_one({'_id': 'classes'})
        return data_classes


@dataclass
class DataUsers:
    _id: int

    async def get_data_user(self):
        data_users = await db.users.find_one({'_id': self._id})
        return data_users

    async def append_user(self):
        pass


class StaticData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __setattr__(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = value

    async def load_data(self):
        self.classes = await DataClasses().get_data_classes
        self.keyboard = await DataKeyboard().get_data_keyboard
