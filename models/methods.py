"""Модуль с методами для работы с БД."""

import motor.motor_asyncio
from config_data.config import load_config

config = load_config()

client = motor.motor_asyncio.AsyncIOMotorClient(
    f'mongodb+srv://Welcome_to_Hell:{config.db.db_password}@cluster0.uh4agnt.mongodb.net/?retryWrites=true&w=majority')
db = client.test_database
collection = db.test_collection
