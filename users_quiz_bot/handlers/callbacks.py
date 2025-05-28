from cProfile import label
from enum import Enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class Level(Enum):
    CATEGORY = 'category'
    SUBCATEGORY = 'subcategory'
    QUIZ_START = 'quiz_start'
    QUIZ = 'quiz'


class CategoryCallback(CallbackData, prefix='cat'):
    id: int


class SubcategoryCallback(CallbackData, prefix='sub'):
    id: int
    category_id: int


class QuizCallback(CallbackData, prefix='quiz'):
    id: int
    subcategory_id: int
    category_id: int


class OptionCallback(CallbackData, prefix='option'):
    id: int
    quiz_id: int
    subcategory_id: int
    category_id: int


class BackCallback(CallbackData, prefix='back'):
    level: str
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    quiz_id: Optional[int] = None


if __name__ == '__main__':
    level = Level("category")
    print(level)