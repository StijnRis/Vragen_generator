# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from urllib.parse import urlparse, parse_qs

import questions


hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("D:/Programmeren/Hulpprogramma/Scheikunde/Vragen_generator/index.html", encoding='utf-8') as file:
                self.wfile.write(bytes(file.read(), 'utf-8'))
        elif self.path[:4] == '/api':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            exam = questions.Exams()
            
            parsed_url = urlparse(self.path)
            query = parse_qs(parsed_url.query)
            all_questions = exam.get_questions_about(query['q'][0])
            all_exam_ids = set(x.exam_id for x in all_questions)
            all_exams = []
            for exam_id in all_exam_ids:
                all_exams.append(questions.Exam(exam_id))
            data = {"questions": all_questions, "exams": all_exams}
            self.wfile.write(bytes(json.dumps(data, default=lambda o: o.__dict__), 'utf-8'))
        else:
            self.send_response(404)


if __name__ == "__main__":
    questions.Database.location = 'D:/Programmeren/Hulpprogramma/Scheikunde/Vragen_generator/questions.db'    
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")