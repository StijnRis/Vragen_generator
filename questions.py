import PyPDF2
import requests
from io import BytesIO
from datetime import datetime
import re
import sqlite3

class Database():
    location = 'D:/Programmeren/Hulpprogramma/Scheikunde/Vragen_generator/test.db'

class Question:
    @staticmethod
    def reset_table():
        conn = sqlite3.connect(Database.location)
        sql = 'DROP TABLE IF EXISTS question'
        conn.execute(sql)
        sql = '''CREATE TABLE question (
            id INTEGER NOT NULL PRIMARY KEY, 
            exam_id INTEGER NOT NULL, 
            question_number INTEGER NOT NULL, 
            question TEXT NOT NULL,
            context TEXT NOT NULL
            );'''
        conn.execute(sql)
        conn.close()
    
    @staticmethod
    def create_new(exam_id: int, number: int, question: str, context: str) -> None:
        conn = sqlite3.connect(Database.location)
        sql = f'INSERT INTO question (exam_id, question_number, question, context) VALUES (?, ?, ?, ?)'
        result = conn.execute(sql, (exam_id, number, question, context))
        id = result.lastrowid
        conn.commit()
        conn.close()
        return Question(id)

    def __init__(self, id: int) -> None:
        self.id = id
        conn = sqlite3.connect(Database.location)
        sql = f'SELECT exam_id, question_number, question, context FROM question WHERE id==?'
        result = conn.execute(sql, (self.id, )).fetchone()
        self.exam_id = result[0]
        self.number = result[1]
        self.question = result[2]
        self.context = result[3]
    
    # def save_question(self):
    #     conn = sqlite3.connect(Database.location)
    #     sql = f'INSERT INTO question (exam_id, question_number, question, context) VALUES (?, ?, ?)'
    #     conn.execute(sql, (self.exam_id, self.number, self.question))
    #     conn.commit()
    #     conn.close()
    

class Exam:
    @staticmethod
    def reset_table():
        conn = sqlite3.connect(Database.location)
        sql = 'DROP TABLE IF EXISTS exam'
        conn.execute(sql)
        sql = '''CREATE TABLE exam (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL, 
            level TEXT NOT NULL, 
            year INTEGER NOT NULL, 
            version INTEGER NOT NULL 
            );'''
        conn.execute(sql)
        conn.close()
    
    @staticmethod
    def create_new(url: str, level: str, year: int, version: int) -> 'Exam':
        conn = sqlite3.connect(Database.location)
        sql = '''INSERT INTO exam (url, level, year, version) VALUES (?, ?, ?, ?);'''
        result = conn.execute(sql, (url, level, year, version))
        exam_id = result.lastrowid
        conn.commit()
        conn.close()
        exam = Exam(exam_id)
        return exam

    def __init__(self, id: int) -> None:
        self.id = id
        conn = sqlite3.connect(Database.location)
        sql = f'SELECT url, level, year, version FROM exam WHERE id==?'
        result = conn.execute(sql, (self.id, )).fetchone()
        self.url = result[0]
        self.level = result[1]
        self.year = result[2]
        self.version = result[3]
        self.questions: list[Question] = []
        self.load_questions()
    
    def find_questions(self) -> list[Question]:
        print(f'Finding questions in {self.url}')
        page = requests.get(self.url, stream=True)
        if page.status_code == 404:
            print('No page was found')
            return
        file = BytesIO(page.content)
        fileReader = PyPDF2.PdfFileReader(file)

        content = ''
        for page in fileReader.pages:
            content += page.extract_text() + '\n'
        with open('test.txt', 'w', encoding="utf-8") as file:
            file.write(content)
        content = re.sub(r'([A-Z]*-){0,1}([a-z0-9-]+) ([0-9 \/]+?) [lL]ees verder( ►►►){0,1}', '\n', content)
        
        self.questions = []
        # matches = re.findall(r'\n[0-9]p ([0-9]+)([\s\S]*?)(?=(\n[0-9]p ([0-9]+))|\Z)', content)
        matches = re.findall(r'\n[0-9]p ([0-9]+)([\s\S]+?[\.?]) *(?=(  |\n *\n|\n[0-9]p|\Z))', content)
        for match in matches:
            context = ""
            number = match[0]
            question = match[1].strip()
            question = Question.create_new(self.id, number, question, context)
            self.questions.append(question)
        
        if len(self.questions) < 10:
            print(f" - Something is propably wrong with this exam, it only had {len(self.questions)} questions")
    
    def load_questions(self) -> list[Question]:
        self.questions = []
        conn = sqlite3.connect(Database.location)
        sql = f'SELECT id FROM question WHERE exam_id==?'
        results = conn.execute(sql, (self.id, ))
        for result in results:
            question = Question(result[0])
            self.questions.append(question)

class Exams:
    def __init__(self) -> None:
        pass

    def get_questions_about(self, query: str) -> list[Question]:
        conn = sqlite3.connect(Database.location)
        subjects = query.split(" ")
        sql = f'SELECT id FROM question WHERE {(" OR ".join("question LIKE ?" for x in range(len(subjects))))} ORDER BY RANDOM() LIMIT 50'
        results = conn.execute(sql, [f'%{subject}%' for subject in subjects])
        questions = []
        for result in results:
            question = Question(result[0])
            questions.append(question)
        return questions

    def find_all_nvon_examens(self) -> list[Exam]:
        urls = [
            # {
            #     'level': 'vmbo',
            #     'url': 'https://newsroom.nvon.nl/files/default/skc{id}vb.pdf'
            # },
            # {
            #     'level': 'vmbo',
            #     'url': 'https://newsroom.nvon.nl/files/default/nask2tl{id}vb.pdf'
            # },
            # {
            #     'level': 'havo',
            #     'url': 'https://newsroom.nvon.nl/files/default/skh{id}vb.pdf'
            # },
            {
                'level': 'vwo',
                'url': 'https://newsroom.nvon.nl/files/default/skv{id}vb.pdf'
            }
        ]
        exams = []
        for url_item in urls:
            for year in range(2010, datetime.today().year):
                for version in range(1,3):
                    id = str(year)[-2:] + str(version)
                    url = url_item['url'].replace('{id}', id)
                    exam = Exam.create_new(url, url_item['level'], year, version)
                    exams.append(exam)
        return exams

def reset():
    Question.reset_table()
    Exam.reset_table()
    exams = Exams()
    novon_exams = exams.find_all_nvon_examens()
    for exam in novon_exams:
        exam.find_questions()

def test():
    conn = sqlite3.connect(Database.location)
    sql = f'SELECT level, year, version, number, question FROM question WHERE question LIKE "%stereo-isomeer%"'
    results = conn.execute(sql)
    count = 0
    for result in results:
        count += 1
        print('\n\n\n')
        print(result)
    print(count)

if __name__ == '__main__':
    reset()
    # a = Exam.create_new('https://newsroom.nvon.nl/files/default/skv162vb.pdf', 'vwo', 2000, 1)
    # a.find_questions()
    # print(a.questions)
    # nvon_exams = NvonExams()
    # exams = nvon_exams.find_all_examens()
    # exams[-1].load_questions()
    # print(exams[-1].questions)
    # test()