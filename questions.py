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
            exam_page_numer INTEGER NOT NULL, 
            question_number INTEGER NOT NULL, 
            question TEXT NOT NULL,
            context TEXT NOT NULL
            );'''
        conn.execute(sql)
        conn.close()
    
    @staticmethod
    def create_new(exam_id: int, page_numer:int, number: int, question: str, context: str) -> None:
        conn = sqlite3.connect(Database.location)
        sql = f'INSERT INTO question (exam_id, exam_page_numer, question_number, question, context) VALUES (?, ?, ?, ?, ?)'
        result = conn.execute(sql, (exam_id, page_numer, number, question, context))
        id = result.lastrowid
        conn.commit()
        conn.close()
        return Question(id)

    def __init__(self, id: int) -> None:
        self.id = id
        conn = sqlite3.connect(Database.location)
        sql = f'SELECT exam_id, exam_page_numer, question_number, question, context FROM question WHERE id==?'
        result = conn.execute(sql, (self.id, )).fetchone()
        self.exam_id = result[0]
        self.exam_page_numer = result[1]
        self.number = result[2]
        self.question = result[3]
        self.context = result[4]
    
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
            print('Pdf was not found')
            return
        file = BytesIO(page.content)
        fileReader = PyPDF2.PdfFileReader(file)

        content = '{webpage 1}'
        for page in fileReader.pages:
            content += page.extract_text() + f'\n {{webpage {fileReader.getPageNumber(page)+2}}}'
        with open('test.txt', 'w', encoding="utf-8") as file:
            file.write(content)
        content = re.sub(r'([A-Z]*-){0,1}([a-z0-9-]+) ([0-9 \/]+?) [lL]ees verder( ►►►){0,1}', '\n', content)
        
        self.questions = []
        matches = re.finditer(r'\n[0-9]p ([0-9]+)([\s\S]+?[\.?]) *(?=(  |\n *\n|\n[0-9]p|\Z))', content)
        parsed_content = content
        page_number = 1
        skipped_questions = 0
        for match in matches:
            index = parsed_content.find(match.group())
            context = parsed_content[:index]
            page_number_match = re.search(r"{webpage (\d+)}", context)
            if page_number_match:
                page_number = int(page_number_match[1])
            parsed_content = parsed_content[index+len(match.group()):]
            question_number = int(match[1])
            question = match[2].strip()
            question = Question.create_new(self.id, page_number, question_number, question, context.strip())
            self.questions.append(question)
            if len(self.questions) + skipped_questions != question_number:
                print(f" - Question {len(self.questions) + skipped_questions} is missing is exam {self.id}. Skipped to question {question_number}")
                skipped_questions = question_number - len(self.questions)
    
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
        sql = f'SELECT id FROM question WHERE {(" OR ".join("question LIKE ?" for x in range(len(subjects))))} OR {(" OR ".join("context LIKE ?" for x in range(len(subjects))))} ORDER BY RANDOM() LIMIT 25'
        arguments = []
        for subject in subjects:
            arguments.append(f'%{subject}%')
            arguments.append(f'%{subject}%')
        results = conn.execute(sql, arguments)
        questions = []
        for result in results:
            question = Question(result[0])
            questions.append(question)
        return questions

    def find_all_nvon_examens(self) -> list[Exam]:
        urls = [
            {
                'level': 'vmbo',
                'url': 'https://newsroom.nvon.nl/files/default/skc{id}vb.pdf'
            },
            {
                'level': 'vmbo',
                'url': 'https://newsroom.nvon.nl/files/default/nask2tl{id}vb.pdf'
            },
            {
                'level': 'havo',
                'url': 'https://newsroom.nvon.nl/files/default/skh{id}vb.pdf'
            },
            {
                'level': 'vwo',
                'url': 'https://newsroom.nvon.nl/files/default/skv{id}vb.pdf'
            }
        ]
        exams = []
        for url_item in urls:
            for year in range(2000, datetime.today().year):
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