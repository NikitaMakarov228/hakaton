from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from queries.sqliteQuery import sqQuery


class ReplyPanel(ReplyKeyboardMarkup):
    choose_sorting_type_list = [
        "Частые вопросы",
        "Последние вопросы",
    ]

    def __init__(self):
        super().__init__()
        self.resize_keyboard = True
        self.one_time_keyboard = True

    def getSortButtons(self) -> ReplyKeyboardMarkup:
        self.keyboard = []
        button_list = []
        for _type in self.choose_sorting_type_list:
            button = KeyboardButton(
                text=_type,
            )
            button_list.append(button)
        self.row(button_list[0], button_list[1])
        return self

    async def getQuestionsPanel(self, questions) -> ReplyKeyboardMarkup:
        self.keyboard = []
        for question in questions:
            button = KeyboardButton(text=f"{question[0]} id вопроса: {question[1]}")
            self.add(button)
        return self


reply = ReplyPanel()
