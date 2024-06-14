from createBot import dp, bot
from aiogram import types, Dispatcher
from keyboards.inline import inline
from queries.postgresQuery import postgres
from keyboards.reply import reply
import asyncio
from aiogram.dispatcher import FSMContext
from dops.states import Parameter, Question
from aiogram.types import InlineKeyboardButton
from queries.sqliteQuery import sqQuery

from funcs.more_funcs import funcsObject

questions = []
keys = []


@dp.message_handler(commands=["start"], state=None)
async def process_start_command(message: types.Message):
    await bot.send_message(
        message.from_user.id, "Привет, я бот проектного офиса пермской вышки"
    )
    await bot.send_message(
        message.from_user.id,
        "Чем могу быть полезен?",
        reply_markup=inline.getCommandButtons(type_panel="student"),
    )
    await asyncio.sleep(1)


async def show_page(chat_id, caption, current_page, pages):
    inline.inline_keyboard = []
    inline.row_width = 2
    back = InlineKeyboardButton(text="⬅️", callback_data="back")
    skip = InlineKeyboardButton(text="➡️", callback_data="skip")
    button = InlineKeyboardButton(
        text=f"{current_page}/{len(pages)}", callback_data="num"
    )
    add = InlineKeyboardButton(text="Задать вопрос", callback_data="command2")
    if len(pages) > 1:
        if current_page == 1:
            inline.row(button, skip)
            inline.add(add)
        elif current_page < len(pages) and current_page > 1:
            inline.row(back, button, skip)
            inline.add(add)
        elif current_page == len(pages):
            inline.row(back, button)
            inline.add(add)
    elif len(pages) == 1:
        inline.add(button)
        inline.add(add)
    msg = await bot.send_message(
        chat_id=chat_id,
        text=caption,
        reply_markup=inline,
    )


@dp.callback_query_handler(text=["skip", "num", "back"])
async def call_data_process(call: types.CallbackQuery):
    global events
    chat_id = call.message.chat.id

    if call.data == "skip":
        pages = list(range(0, len(events)))
        msg = call.message.message_id
        data = call.message.reply_markup.inline_keyboard
        data_1 = None
        for i in data:
            for k in i:
                k = dict(k)
                k = list(k.values())
                for v in k:
                    if v == "num":
                        data_1 = k[0]
        if data_1 == None:
            current_page = 1
        else:
            current_page = int((data_1.split("/"))[0])
        current_page += 1
        caption = funcsObject.getDescription(current_page, events)
        await bot.delete_message(chat_id=chat_id, message_id=msg)
        await show_page(call.message.chat.id, caption, current_page, pages)

    elif call.data == "num":
        await call.answer(
            "Эта кнопка демонстрирует позицию предложения в списке рекомендаций",
            show_alert=True,
        )
    elif call.data == "back":
        pages = list(range(0, len(events)))
        msg = call.message.message_id
        data = call.message.reply_markup.inline_keyboard
        data_1 = None
        for i in data:
            for k in i:
                k = dict(k)
                k = list(k.values())
                for v in k:
                    if v == "num":
                        data_1 = k[0]
        if data_1 == None:
            current_page = 1
        else:
            current_page = int((data_1.split("/"))[0])
        current_page -= 1
        caption = funcsObject.getDescription(current_page, events)
        await bot.delete_message(chat_id=chat_id, message_id=msg)
        await show_page(call.message.chat.id, caption, current_page, pages)


@dp.callback_query_handler(text=["command0", "command1", "command2"])
async def call_data_process(callback: types.CallbackQuery):
    global events
    match callback.data:
        case "command0":
            events = funcsObject.read_json_file()
            pages = list(range(0, len(events)))
            current_page = 1
            caption = funcsObject.getDescription(current_page, events)
            await bot.send_sticker(
                callback.from_user.id,
                sticker="CAACAgIAAxkBAAEL3OFmEoC4Tecisl_BaFx8CUSC9RMipwACaB4AAlXrsElJvF10IIvl4TQE",
            )

            await show_page(callback.message.chat.id, caption, current_page, pages)
        case "command1":
            await bot.send_sticker(
                callback.from_user.id,
                sticker="CAACAgIAAxkBAAEL3ONmEoDa1f3f8TMI0l7Iyvlh37IvLAAChh4AAli2uUmKyhwk5cx2CjQE",
            )

            await bot.send_message(
                callback.from_user.id,
                "Выберите в документе свободное для записи время",
                reply_markup=inline.addHref(),
            )
        case "command2":
            await bot.send_message(
                callback.from_user.id,
                "Может твой вопрос есть в списке?\nВыбери, по какому критерию отобрать",
                reply_markup=reply.getSortButtons(),
            )
            await Parameter.parameter.set()


@dp.callback_query_handler(text=["None", "own_question"])
async def call_data_process(callback: types.CallbackQuery):
    match callback.data:
        case "None":
            questions_split = [i[0] for i in questions]
            inline.number_of_elements_to_show = 5
            while True:
                [array, flag] = funcsObject.getSlice(
                    questions_split, inline.number_of_elements_to_show
                )
                await bot.send_message(
                    callback.from_user.id,
                    "Далее:",
                    reply_markup=inline.getQuestions(array, questions_split, flag),
                )
                inline.number_of_elements_to_show += 5
                if flag:
                    # логика оканчивания
                    break
        case "own_question":
            await bot.send_message(
                callback.from_user.id,
                "Введи свой вопрос (возможно придется немного подождать, работает нейросеть)",
            )
            await Question.question.set()


@dp.callback_query_handler(lambda callback: callback.data in keys)
async def call_data_process(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[1])
    answer = questions[index][1]
    await postgres.updateQuestion(questions[index][0])
    await bot.send_message(
        callback.from_user.id,
        f"Ответ найден: {answer}",
    )


@dp.message_handler(content_types=["question"], state=Question.question)
async def getQuestion(message: types.Message, state: FSMContext):
    global questions
    async with state.proxy() as data:
        data["question"] = message.text
    flag = False
    for i in questions:
        isValid = await funcsObject.isValidQuestion(data["question"], i)
        if isValid:
            flag = True
            await bot.send_message(
                message.from_user.id,
                f"Ответ найден: {i[1]}",
            )
            await state.finish()
            break
    if not flag:
        await bot.send_message(
            message.from_user.id,
            f"Увы, я не нашел похожий вопрос. Отправляю его в проектный офис",
        )
        await sqQuery.addQuestion(
            [message.from_user.id, message.message_id, data["question"], "null"]
        )
        await state.finish()


@dp.message_handler(content_types=["parameter"], state=Parameter.parameter)
async def getParameter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["parameter"] = message.text

    match data["parameter"]:
        case "Частые вопросы":
            parameter = True
        case "Последние вопросы":
            parameter = False
        case _:
            parameter = None

    if type(parameter) == bool:
        global questions
        questions = await postgres.getQuestionInfos(parameter)
        questions_split = [i[0] for i in questions]
        [array, flag] = funcsObject.getSlice(
            questions_split, inline.number_of_elements_to_show
        )
        await bot.send_message(
            message.from_user.id,
            f"{data['parameter']}:",
            reply_markup=inline.getQuestions(array, array, flag),
        )
        global keys
        keys = [f"question_{questions_split.index(i)}" for i in questions_split]
        await state.finish()

    else:
        await state.finish()
        await bot.send_message(
            message.from_user.id,
            "Всё таки попробуй)",
            reply_markup=reply.getSortButtons(),
        )
        await Parameter.parameter.set()
