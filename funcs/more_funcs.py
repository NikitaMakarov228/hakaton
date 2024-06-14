from funcs.gpt_request import gptReq
import json
from createBot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


class Funcs:

    @staticmethod
    def sortQuestions(array: list) -> list:
        ready_list = [list(arr) for arr in array]
        return ready_list

    @staticmethod
    def getSlice(array: list, number: int) -> [list, bool]:
        if len(array) == 0 or number >= len(array):
            return [[], True]

        last_index = min(number + 5, len(array))
        this_slice = array[number:last_index]
        flag = last_index == len(array)
        return [this_slice, flag]

    @staticmethod
    async def isValidQuestion(question: str, question_2: list) -> bool:
        prompt = f"Существует два вопроса: {question} и {question_2[0]}. Отправь мне только слово True, если эти вопросы взаимозаменяемые, либо только False, если эти вопросы не взаимозаменяемые."
        result = await gptReq(prompt)
        match result:
            case "True":
                answer = question_2[1]
            case _:
                answer = None
        return answer

    @staticmethod
    def getDescription(current_page: int, events: list) -> str:
        result = events[current_page - 1]
        string = f"Стажировка в {result[0]}\n\n{result[1]}\n\n{result[2]}"
        return string

    @staticmethod
    def read_json_file() -> list:
        file_path = "json/tableData.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                companies_info = [
                    [company[0], company[1], company[2]] for company in data
                ]

                return companies_info
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    @staticmethod
    async def Cancel(state: FSMContext, answer: [types.Message, types.CallbackQuery]):
        await bot.send_message(
            answer.from_user.id, "Выберите, что необходимо сделать дальше!"
        )
        await state.finish()


funcsObject = Funcs()
