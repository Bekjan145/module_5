import asyncio
import logging
import sys
import psycopg2
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import html
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")


conn = psycopg2.connect(
    dbname="register_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    age INTEGER CHECK (age > 0),
    phone_number TEXT NOT NULL
);
""")
conn.commit()

# FSM holatlari
class Registration(StatesGroup):
    fullname = State()
    age = State()
    phone = State()

# Dispatcher
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (message.from_user.id,))
    user = cursor.fetchone()

    if user:
        await message.answer(f"Welcome back, {html.bold(user[1])}! Let's start the game.")
        # O'yinni shu yerda boshlash mumkin
    else:
        await message.answer("Xush kelibsiz! To'liq ismingiz nima?")
        await state.set_state(Registration.fullname)

@dp.message(Registration.fullname)
async def process_fullname(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("Yoshingiz nechida?")
    await state.set_state(Registration.age)

@dp.message(Registration.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Raqam kiriting:")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Telefon raqamingizni kiriting:")
    await state.set_state(Registration.phone)

@dp.message(Registration.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()

    # Ma'lumotlarni PostgreSQL bazasiga yozish
    cursor.execute(
        "INSERT INTO users (full_name, age, phone_number) VALUES (%s, %s, %s)",
        (data['full_name'], data['age'], phone)
    )
    conn.commit()

    await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz! Keling, o'yinni boshlaymiz.")
    await state.clear()
    # O‘yin shu yerda boshlanadi

# Botni ishga tushurish
async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
























