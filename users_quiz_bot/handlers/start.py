from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from users_quiz_bot.database.quiz_db import PostgresSQL
from users_quiz_bot.handlers.callbacks import CategoryCallback

start_router = Router()
db = PostgresSQL()

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db.register(message.chat.id, message.from_user.full_name)
    categories = db.get_category()
    builder = InlineKeyboardBuilder()
    for text, cat_id in categories:
        builder.button(text=text, callback_data=CategoryCallback(id=cat_id))
    builder.adjust(2)
    await message.answer(
        f"Salom, {html.bold(message.from_user.full_name)}!\n\n"
            f"Bo'limni tanlang:",
             reply_markup=builder.as_markup()
    )