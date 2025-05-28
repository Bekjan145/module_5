from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from users_quiz_bot.database.quiz_db import PostgresSQL
from users_quiz_bot.handlers.callbacks import CategoryCallback, SubcategoryCallback, BackCallback, Level, QuizCallback, OptionCallback

router = Router()
db = PostgresSQL()

user_quiz_data = {}


@router.callback_query(CategoryCallback.filter())
async def handle_category_callback(call: CallbackQuery, callback_data: CategoryCallback):
    subcategories = db.get_subcategory(callback_data.id)
    builder = InlineKeyboardBuilder()
    for text, sub_id in subcategories:
        builder.button(text=text, callback_data=SubcategoryCallback(id=sub_id, category_id=callback_data.id))
    builder.button(
        text="⬅️ Ortga",
        callback_data=BackCallback(level=Level.CATEGORY.value)
    )
    builder.adjust(2)
    await call.message.edit_text(
        text=f"Bolim ichidagi mavzular:", reply_markup=builder.as_markup()
    )


@router.callback_query(SubcategoryCallback.filter())
async def show_quiz_start(call: CallbackQuery, callback_data: SubcategoryCallback):
    quizzes = db.get_quiz(callback_data.id)

    user_id = call.from_user.id
    user_quiz_data[user_id] = {
        'category': callback_data.category_id,
        'subcategory': callback_data.id,
        'quizzes': quizzes,
        'current_index': 0,
        'correct_answers': 0,
        'user_answers': {}
    }

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Testni boshlash 🚀",
        callback_data=QuizCallback(id=quizzes[0][1], subcategory_id=callback_data.id, category_id=callback_data.category_id)
    )
    builder.button(
        text="⬅️ Ortga",
        callback_data=BackCallback(
            level=Level.SUBCATEGORY.value,
            category_id=callback_data.category_id
        )
    )
    builder.adjust(1)
    await call.message.edit_text(
        f"Test {len(quizzes)} ta savoldan iborat. Boshlaymizmi?",
        reply_markup=builder.as_markup()
    )


@router.callback_query(QuizCallback.filter())
async def show_question(call: CallbackQuery, callback_data: QuizCallback):
    user_id = call.from_user.id

    quiz_data = user_quiz_data[user_id]
    quizzes = quiz_data['quizzes']
    current_index = quiz_data['current_index']

    question_text = db.get_question_text(callback_data.id)
    options = db.get_option(callback_data.id)

    builder = InlineKeyboardBuilder()
    for text, option_id in options:
        builder.button(
            text=text,
            callback_data=OptionCallback(
                id=option_id,
                quiz_id=callback_data.id,
                subcategory_id=callback_data.subcategory_id,
                category_id=callback_data.category_id
            )
        )
    builder.adjust(2)
    await call.message.edit_text(
        f"Savol {current_index + 1}/ {len(quizzes)}:\n\n{question_text}",
        reply_markup=builder.as_markup()
    )


@router.callback_query(OptionCallback.filter())
async def process_answer(call: CallbackQuery, callback_data: OptionCallback):
    user_chat_id = call.from_user.id

    quiz_data = user_quiz_data[user_chat_id]
    quizzes = quiz_data['quizzes']
    current_index = quiz_data['current_index']
    quiz_id = callback_data.quiz_id

    selected_option = db.get_option(quiz_id, callback_data.id)
    is_correct = selected_option[1]

    quiz_data['user_answers'][quiz_id] = callback_data.id
    user_id = db.find_id_by_chat_id(chat_id=user_chat_id)
    db.save_answer(user_id=user_id, quiz_id=callback_data.quiz_id, option_id=callback_data.id)
    if is_correct:
        quiz_data['correct_answers'] += 1

    if current_index + 1 < len(quizzes):
        quiz_data['current_index'] += 1
        next_quiz_id = quizzes[current_index + 1][1]
        await show_question(
            call,
            QuizCallback(
                id=next_quiz_id,
                subcategory_id=callback_data.subcategory_id,
                category_id=callback_data.category_id
            )
        )
    else:
        total_questions = len(quizzes)
        correct_answer = quiz_data['correct_answers']
        score = f"{correct_answer}/{total_questions}"
        builder = InlineKeyboardBuilder()
        builder.button(
            text="Testni qayta boshlash 🔄",
            callback_data=SubcategoryCallback(
                id=quiz_data['subcategory'],
                category_id=quiz_data['category']
            )
        )
        builder.button(
            text="Bosh menyu 🏠",
            callback_data=BackCallback(level=Level.CATEGORY.value)
        )
        builder.adjust(1)
        await call.message.edit_text(
            f"Test yakunlandi! Natijangiz: {score}\n\nYana test yechmoqchimisiz?",
            reply_markup=builder.as_markup()
        )




@router.callback_query(BackCallback.filter())
async def handle_back_callback(call: CallbackQuery, callback_data: BackCallback):
    level = Level(callback_data.level)

    if level == Level.CATEGORY:
        categories = db.get_category()
        builder = InlineKeyboardBuilder()
        for text, cat_id in categories:
            builder.button(text=text, callback_data=CategoryCallback(id=cat_id))
        builder.adjust(2)
        await call.message.edit_text(
            text="Bo‘limni tanlang:",
            reply_markup=builder.as_markup()
        )

    elif level == Level.SUBCATEGORY:
        subcategories = db.get_subcategory(callback_data.category_id)
        builder = InlineKeyboardBuilder()
        for text, sub_id in subcategories:
            builder.button(text=text, callback_data=SubcategoryCallback(id=sub_id, category_id=callback_data.category_id))
        builder.button(
            text="⬅️ Ortga",
            callback_data=BackCallback(level=Level.CATEGORY.value)
        )
        builder.adjust(2)
        await call.message.edit_text(
            text="Bo‘lim ichidagi mavzular:", reply_markup=builder.as_markup()
        )



