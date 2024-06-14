from createBot import dp
from handlers.student_handler import process_start_command, getParameter, getQuestion
from handlers.admin_handler import (
    admin_start_command,
    getConcultUrl,
    getTableHref,
    getAnswerOnQuestion,
    chooseQuestion,
)
from dops.states import (
    AnswerQuestion,
    Question,
    Consultation,
    Parameter,
    TableData,
    Photo,
    Answer,
)


def register_handlers_client(dp):
    dp.register_message_handler(process_start_command, commands=["start"])
    dp.register_message_handler(getParameter, state=Parameter.parameter)
    dp.register_message_handler(getQuestion, state=Question.question)
    dp.register_message_handler(getConcultUrl, state=Consultation.url)
    dp.register_message_handler(getTableHref, state=TableData.url)
    dp.register_message_handler(admin_start_command, commands=["adminfunctional"])
    dp.register_message_handler(getAnswerOnQuestion, state=Answer.answer)
    dp.register_message_handler(chooseQuestion, state=AnswerQuestion.question)
