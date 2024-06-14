from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import json


class InlinePanel(InlineKeyboardMarkup):
    choose_command_list = [
        "Просмотреть стажировки и мероприятия",
        "Записаться на консультацию",
        "Задать вопрос",
    ]

    admin_command_list = [
        "Изменить ссылку на записи на консультации",
        "Изменить ссылку на таблицу со стажировками",
        "Ответить на вопросы студентов",
    ]

    number_of_elements_to_show = 0
    href = "https://docs.google.com/spreadsheets/d/1N6N6WokY8aSUYMj6DGZe7JgJCg71azYbnGE2RjMrYaM/edit#gid=0"

    def __init__(self):
        super().__init__()

    def getCommandButtons(self, type_panel) -> InlineKeyboardMarkup:
        self.inline_keyboard = []

        match type_panel:
            case "admin":
                self.row_width = len(self.admin_command_list)
                for command in self.admin_command_list:
                    button = InlineKeyboardButton(
                        text=f"{command}",
                        callback_data=f"admincommand{self.admin_command_list.index(command)}",
                    )
                    self.add(button)
            case "student":
                self.row_width = len(self.choose_command_list)
                for command in self.choose_command_list:
                    button = InlineKeyboardButton(
                        text=f"{command}",
                        callback_data=f"command{self.choose_command_list.index(command)}",
                    )
                    self.add(button)
        return self

    def getQuestions(
        self, array: list, bigger_array: list, flag: bool
    ) -> InlineKeyboardMarkup:
        self.inline_keyboard = []

        self.row_width = len(array)
        for question in array:
            button = InlineKeyboardButton(
                text=f"{question}",
                callback_data=f"question_{bigger_array.index(question)}",
            )
            self.add(button)
        if not flag:
            show_more_button = InlineKeyboardButton(
                text="Показать еще...",
                callback_data="None",
            )
            own_question_button = InlineKeyboardButton(
                text="Свой вопрос",
                callback_data="own_question",
            )
            self.row(show_more_button, own_question_button)
        return self

    @staticmethod
    def getTableHrefFromJson() -> str:
        file_path = "json\consultUrl.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    def addHref(self) -> InlineKeyboardMarkup:
        self.inline_keyboard = []

        button = InlineKeyboardButton(
            text=f"Кликните для перехода по ссылке", url=self.getTableHrefFromJson()
        )
        self.add(button)
        return self

    def cancelButton(self) -> InlineKeyboardMarkup:
        self.inline_keyboard = []
        button = InlineKeyboardButton(text=f"Отмена", callback_data="cancel")
        self.add(button)
        return self

    def answerQuestion(self, question_id) -> InlineKeyboardMarkup:
        self.inline_keyboard = []
        button = InlineKeyboardButton(
            text="Ответить", callback_data=f"answerQuestion{question_id}"
        )
        self.add(button)
        return self


inline = InlinePanel()
