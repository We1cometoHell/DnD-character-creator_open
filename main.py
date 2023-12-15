from aiogram import Dispatcher, Bot
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, Command
from aiogram.types import ChatMemberUpdated, Message
import motor.motor_asyncio
from config_data.config import load_config

config = load_config()

client = motor.motor_asyncio.AsyncIOMotorClient(
    f'mongodb+srv://Welcome_to_Hell:{config.db.db_password}@cluster0.uh4agnt.mongodb.net/?retryWrites=true&w=majority')
db = client.test_database
collection = db.test_collection

bot = Bot(config.tg_bot.bot_token)  # Создает бота по ключу, ключ хранится в отдельном файле
dp = Dispatcher()  # Основной, на данный момент, способ взаимодейтсвия с апдейтами от пользователя


class BaseDate:
    """Данный класс предназначен для хранения информации,
    которая позже будет перенесена в базу данных"""

    _character_classes_ru = ["Бард", "Варвар", "Воин", "Волшебник", "Друид", "Жрец", "Изобретатель", "Колдун", "Монах",
                             "Паладин", "Плут", "Следопыт", "Чародей"]
    _character_classes_en = ["Bard", "Barbarian", "Fighter", "Wizard", "Druid", "Cleric", "Artificer", "Warlock",
                             "Monk",
                             "Paladin", "Rogue", "Ranger", "Sorcerer"]


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(text='Вы запустили бота')


# Этот хэндлер будет срабатывать на блокировку бота пользователем, пока что в таком виде
@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f'Пользователь {event.from_user.id} заблокировал бота')


if __name__ == '__main__':
    dp.run_polling(bot)
