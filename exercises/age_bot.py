import asyncio
import logging
import sys
from os import getenv
from datetime import datetime


from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(F.text.regexp(r"^\d{4}-\d{2}-\d{2}$"))
async def year_to_age_handler(message: Message) -> None:
    text = message.text.strip()
    try:
        birth_date = datetime.strptime(text, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        await message.answer(f"Siz {age} yoshdasiz.")
    except ValueError:
        await message.answer("Tug‘ilgan kuningizni YYYY-MM-DD formatida kiriting")


@dp.message(F.text.regexp(r"^\d{1,3}$"))
async def age_handler(message: Message) -> None:
    try:
        age = int(message.text.strip())
        now_year = datetime.today().year
        if 1 <= age <= 100:
            year = now_year - age
            await message.answer(f"Siz {year} yilga tug`ilgansiz")
    except ValueError:
        await message.answer("Yoshingizni 1 dan 100 gacha kiriting")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
