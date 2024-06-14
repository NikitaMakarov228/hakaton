import psycopg2
from sqlalchemy import text
from funcs.more_funcs import funcsObject
from datetime import datetime


class PostgreSQLQuery:
    conn = psycopg2.connect(
        host="localhost",
        database="QuestionsProjectOfficeDB",
        user="postgres",
        password="89504589467",
    )
    cur = conn.cursor()

    async def getQuestionInfos(self, parameter: bool) -> list():
        param = "Popularity" if parameter else "DateTime"
        query = 'SELECT "Question", "Answer" FROM public."QuestionInfos" ORDER BY "QuestionInfos"."{}" DESC'.format(
            param
        )

        answer = self.cur.execute(query)
        answer = self.cur.fetchall()
        return funcsObject.sortQuestions(answer)

    async def addQuestion(self, question, answer):
        insert_query = 'INSERT INTO public."QuestionInfos" ("Question", "Answer", "Popularity", "DateTime") VALUES (%s, %s,%s, %s);'

        params = (question, answer, 0, datetime.now())
        self.cur.execute(insert_query, params)
        self.conn.commit()

    async def updateQuestion(self, question):
        update_query = 'UPDATE public."QuestionInfos" SET "Popularity" = "Popularity" + 1, "DateTime" = %s WHERE "Question" = %s;'
        params = (datetime.now(), question)
        self.cur.execute(update_query, params)
        self.conn.commit()


postgres = PostgreSQLQuery()
