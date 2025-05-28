# import asyncio
# import logging
# import sys
# from os import getenv
#
# import psycopg2
# from aiogram import Bot, Dispatcher, html, F
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart, Command
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton,
# from dotenv import load_dotenv
#
# load_dotenv()
# TOKEN = getenv("BOT_TOKEN")
#
# dp = Dispatcher(storage=MemoryStorage())
#
#
# class GameStates(StatesGroup):
#     confirming = State()
#     playing = State()
#     finished = State()
#
#
# def make_keyboard(options, row=2):
#     keyboard = [KeyboardButton(text=o) for o in options]
#     buttons = [keyboard[i:i + row] for i in range(0, len(keyboard), row)]
#     return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
#
#
# def get_questions():
#     with psycopg2.connect(
#         dbname=getenv("DB_NAME"),
#         user=getenv("DB_USER"),
#         password=getenv("DB_PASSWORD"),
#         host=getenv("DB_HOST"),
#         port=getenv("DB_PORT")
#     ) as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 SELECT q.text, array_agg(o.text ORDER BY o.id),
#                        MAX(CASE WHEN o.is_correct THEN o.text END)
#                 FROM quiz q
#                 JOIN option o ON q.id = o.quiz_id
#                 GROUP BY q.text
#                 ORDER BY q.text
#                 LIMIT 5;
#             """)
#             rows = cur.fetchall()
#             return [
#                 {"text": row[0], "options": row[1], "correct": row[2]}
#                 for row in rows
#             ]
#
#
# @dp.message(CommandStart())
# async def start_handler(message: Message, state: FSMContext) -> None:
#     await state.clear()
#     await message.answer(
#         f"Salom, {html.bold(message.from_user.full_name)}!\n\n"
#         f"O‘ynash uchun /play buyrug‘ini bosing!",
#         reply_markup=ReplyKeyboardRemove()
#     )
#
#
# @dp.message(Command('play'))
# async def play_handler(message: Message, state: FSMContext):
#     qs = get_questions()
#
#     await state.update_data(questions=qs, total=len(qs), step=0, correct=0)
#     await state.set_state(GameStates.confirming)
#     await message.answer(
#         f"Test {len(qs)} ta savoldan iborat.\nBoshlaymizmi?",
#         reply_markup=make_keyboard(["Ha", "Yoq"])
#     )
#
#
# @dp.message(GameStates.confirming, F.text.in_(["Ha", "Yoq"]))
# async def confirm_handler(message: Message, state: FSMContext):
#     if message.text == "Yoq":
#         await state.clear()
#         await message.answer(
#             "O‘yinni boshlash uchun /play buyrug‘ini bosing.",
#             reply_markup=ReplyKeyboardRemove()
#         )
#         return
#
#     await state.set_state(GameStates.playing)
#     await send_question(message, state)
#
#
# async def send_question(message: Message, state: FSMContext):
#     data = await state.get_data()
#     step = data["step"]
#     correct = data['correct']
#     total = data["total"]
#     questions = data["questions"]
#
#     if step >= total:
#         await message.answer(
#             f"Test yakunlandi!\nTo‘g‘ri javoblar soni: {correct}/{total}\n"
#             f"Yana o‘ynash uchun /play ni bosing.",
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await state.clear()
#         return
#
#     q = questions[step]
#     await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))
#
#
# @dp.message(GameStates.playing)
# async def handler_answer(message: Message, state: FSMContext):
#     data = await state.get_data()
#     step = data["step"]
#     total = data["total"]
#     questions = data["questions"]
#     correct = data["correct"]
#
#     if step >= total:
#         await state.set_state(GameStates.finished)
#         await message.answer("Test tugagan. /play buyrug‘ini bosing.")
#         return
#
#     question = questions[step]
#     if message.text == question["correct"]:
#         correct += 1
#         await message.answer("✅ To‘g‘ri!")
#     else:
#         await message.answer(f"❌ Noto‘g‘ri! To‘g‘ri javob: {question['correct']}")
#
#     await state.update_data(step=step + 1, correct=correct)
#     await send_question(message, state)
#
#
# async def main() -> None:
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
