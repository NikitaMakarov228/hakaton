import sqlite3 as sq
from createBot import bot
from aiogram import types, Dispatcher
from keyboards.inline import inline
from funcs.adminFuncs import admin
from queries.postgresQuery import postgres


class sqliteQuery:
    db = sq.connect("db.db", timeout=15)
    cur = db.cursor()

    def createTable(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS question(question_id TEXT PRIMARY KEY,  question TEXT, context TEXT)"
        )
        self.db.commit()

    async def addQuestion(self, params: list):
        question_id = f"{params[0]}.{params[1]}"
        params = (question_id, params[2], params[3])
        self.cur.execute(
            "INSERT INTO question VALUES(?,?,?)",
            (params),
        )
        self.db.commit()
        admins = admin.get_admin_ids()
        for id in admins:
            await bot.send_message(
                id,
                f"Студент задал вам вопрос!\n{params[1]}",
                reply_markup=inline.answerQuestion(question_id),
            )

    async def getAllQuestions(self) -> list:
        questions = self.cur.execute(
            "SELECT question, question_id FROM question"
        ).fetchall()
        return list(questions)

    async def deleteQuestion(self, question_id, answer):
        params = (question_id,)
        question = self.cur.execute(
            "SELECT question FROM question WHERE question_id = ?", params
        ).fetchone()[0]
        self.cur.execute("DELETE FROM question WHERE question_id = ?", params)
        self.db.commit()
        await postgres.addQuestion(question, answer)


sqQuery = sqliteQuery()
sqQuery.createTable()
