import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import DatabaseHandler

# Укажите ваш токен бота
TOKEN = "8173866226:AAH7k9AEjHMdEMzgjcs_M2LJFdHQmKz6KzY"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "Не указан"
    full_name = message.from_user.full_name

    user_data = DatabaseHandler.get_user(user_id)

    if user_data:
        await message.answer(f"Привет, {full_name}! Ты уже в базе данных. Вот твои данные:\n\n{user_data}")
    else:
        user_file_content = DatabaseHandler.add_user(user_id, username, full_name, bot)
        await message.answer(f"Привет, {full_name}! Ты добавлен в базу данных.")
        if user_file_content:
            await message.answer(f"Ключи OpenVPN для {username} успешно созданы.")


def run():
    asyncio.run(main())

async def main():
    await dp.start_polling(bot)

def run():
    asyncio.run(main())