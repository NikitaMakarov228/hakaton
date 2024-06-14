from createBot import dp, bot
from aiogram import types, Dispatcher
from keyboards.inline import inline
from keyboards.reply import reply
from queries.postgresQuery import postgres
from keyboards.reply import ReplyPanel
import asyncio
from aiogram.dispatcher import FSMContext
from dops.states import AnswerQuestion, Consultation, TableData, Photo, Answer
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from funcs.more_funcs import funcsObject
import json
from funcs.adminFuncs import admin
from queries.sqliteQuery import sqQuery
import re

question_id = {}


@dp.message_handler(commands=["adminfunctional"], state=None)
async def admin_start_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "Здравствуйте, чем могу быть полезен?",
        reply_markup=inline.getCommandButtons(type_panel="admin"),
    )
    admin_id = message.from_user.id
    await admin.set_admin_id(admin_id)
    await asyncio.sleep(1)


@dp.callback_query_handler(
    text=["admincommand0", "admincommand1", "admincommand2", "admincommand3"]
)
async def call_data_process(callback: types.CallbackQuery):
    match callback.data:
        case "admincommand0":
            await bot.send_message(
                callback.from_user.id,
                "Отправьте мне новую ссылку для записи на консультацию",
                reply_markup=inline.cancelButton(),
            )
            await Consultation.url.set()
        case "admincommand1":
            await bot.send_message(
                callback.from_user.id,
                "Отправьте мне новую ссылку на таблицу со стажировками/мероприятиями",
                reply_markup=inline.cancelButton(),
            )
            await TableData.url.set()

        case "admincommand2":
            await bot.send_message(
                callback.from_user.id,
                "Выберите стажировку:",
                reply_markup=inline.cancelButton(),
            )
            await Photo.photo.set()

        case "admincommand3":
            questions = await sqQuery.getAllQuestions()
            if len(questions) != 0:
                await bot.send_message(
                    callback.from_user.id,
                    "Выберите вопрос для ответа:",
                    reply_markup=await reply.getQuestionsPanel(questions),
                )
                await AnswerQuestion.question.set()
            else:
                await bot.send_message(
                    callback.from_user.id,
                    "Новых вопросов от студентов не поступало!",
                )


@dp.callback_query_handler(
    text=["cancel"],
    state=[
        Photo.photo,
        TableData.url,
        Consultation.url,
        Answer.answer,
    ],
)
async def call_data_process(callback: types.CallbackQuery, state: FSMContext):
    await funcsObject.Cancel(state=state, answer=callback)


@dp.message_handler(content_types=["url"], state=Consultation.url)
async def getConcultUrl(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["url"] = message.text
    with open("json\consultUrl.json", "w", encoding="utf-8") as json_file:
        json.dump(data["url"], json_file)
    await bot.send_message(message.from_user.id, "Ссылка обновлена!")
    await state.finish()


@dp.message_handler(content_types=["url"], state=TableData.url)
async def getTableHref(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["url"] = message.text
    with open("json\hrefTable.json", "w", encoding="utf-8") as json_file:
        json.dump(data["url"], json_file)
    await bot.send_message(message.from_user.id, "Ссылка обновлена!")
    await state.finish()


@dp.callback_query_handler(lambda callback: callback.data.startswith("answerQuestion"))
async def call_data_process(callback: types.CallbackQuery):
    global question_id
    question_id[callback.from_user.id] = callback.data.replace("answerQuestion", "")
    await bot.send_message(
        callback.from_user.id,
        "Введите ответ на вопрос:",
        reply_markup=inline.cancelButton(),
    )
    await Answer.answer.set()


@dp.message_handler(content_types=["answer"], state=Answer.answer)
async def getAnswerOnQuestion(message: types.Message, state: FSMContext):
    global question_id
    async with state.proxy() as data:
        data["answer"] = message.text

    student_id = question_id[message.from_user.id].split(".")[0]

    await bot.send_message(message.from_user.id, "Ответ отправлен!")
    await bot.send_message(
        student_id, f'Ответ на ранее заданный вами вопрос:\n{data["answer"]}'
    )
    await sqQuery.deleteQuestion(question_id[message.from_user.id], data["answer"])
    await state.finish()


@dp.message_handler(content_types=["question"], state=AnswerQuestion.question)
async def chooseQuestion(message: types.Message, state: FSMContext):
    global question_id
    async with state.proxy() as data:
        data["question"] = message.text

    match = re.search(r"id вопроса: (\d+\.\d+)", data["question"])
    question_id[message.from_user.id] = match.group(1)
    await bot.send_message(
        message.from_user.id,
        "Введите ответ на вопрос:",
        reply_markup=inline.cancelButton(),
    )
    await state.finish()
    await Answer.answer.set()
