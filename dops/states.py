from aiogram.dispatcher.filters.state import State, StatesGroup


class Parameter(StatesGroup):
    parameter = State()


class Question(StatesGroup):
    question = State()


class Consultation(StatesGroup):
    url = State()


class TableData(StatesGroup):
    url = State()


class Photo(StatesGroup):
    photo = State()


class AnswerQuestion(StatesGroup):
    question = State()


class Answer(StatesGroup):
    answer = State()
