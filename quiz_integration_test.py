import unittest
import flask_testing
import json
from lms import app, db, Quiz, Lesson

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    maxDiff = None

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestQuizzes(TestApp):

    #test create quiz 
    def test_create_quiz(self):
        
        request_body = {
            "lessonId":  1,
            "isGraded": 1,
            "passingMark": 5,
            "numOfQns": 10,
            "quizLink": "https://quiz-maker.com/1",
            "isActive": 'True'
        }

        response = self.client.post("/quiz/add",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "data":{
                "quizId": 1,
                "lessonId": 1,
                "isGraded": 1,
                "passingMark": 5,
                "numOfQns": 10,
                "quizLink": "https://quiz-maker.com/1",
                "isActive": 'True'
            }
        })

    #test view/read quiz
    def test_view_quiz_by_quizId(self):
        q1 = Quiz(quizId = 1, lessonId = 1, isGraded = 1,
                    passingMark = 5, numOfQns = 10, quizLink = "https://quiz-maker.com/1", isActive = 'True')
        db.session.add(q1)
        db.session.commit()

        response = self.client.get("/quiz/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "data":{
                "quizId": 1,
                "lessonId": 1,
                "isGraded": 1,
                "passingMark": 5,
                "numOfQns": 10,
                "quizLink": "https://quiz-maker.com/1",
                "isActive": 'True'
            }
        })

    #test get all quizzes with the same lessonId
    def test_get_quiz_by_lessonId(self):
        l1 = Lesson(courseClassId = 1, lessonName = 'abc',
                    lessonContent = "abc||123||lol", links = "www.google.com||www.googledrive.com")
        db.session.add(l1)
        q1 = Quiz(quizId = 1, lessonId = 1, isGraded = 1,
                    passingMark = 5, numOfQns = 10, quizLink = "https://quiz-maker.com/1", isActive = 'True')
        q2 = Quiz(quizId = 2, lessonId = 1, isGraded = 1,
                    passingMark = 7, numOfQns = 14, quizLink = "https://quiz-maker.com/2", isActive = 'False')
        db.session.add(q1)
        db.session.add(q2)
        db.session.commit()

        response = self.client.get("/quiz/lessonId/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "data":{
                "name": 'abc',
                "quizzes": [
                    {
                        "quizId": 1,
                        "lessonId": 1,
                        "isGraded": 1,
                        "passingMark": 5,
                        "numOfQns": 10,
                        "quizLink": "https://quiz-maker.com/1",
                        "isActive": "True"
                    },
                    {
                        "quizId": 2,
                        "lessonId": 1,
                        "isGraded": 1,
                        "passingMark": 7,
                        "numOfQns": 14,
                        "quizLink": "https://quiz-maker.com/2",
                        "isActive": "False"
                    }
                ]
            }
        })
    
    #test delete quiz 
    def test_delete_quiz(self):
        q1 = Quiz(quizId = 1, lessonId = 1, isGraded = 1,
                    passingMark = 5, numOfQns = 10, quizLink = "https://quiz-maker.com/1", isActive = 'True')
        db.session.add(q1)
        db.session.commit()

        response = self.client.post("/quiz/delete/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Quiz was successfully deleted."
        })
    
    #test update existing quiz
    def test_update_quiz(self):
        q1 = Quiz(quizId = 1, lessonId = 1, isGraded = 1,
                    passingMark = 5, numOfQns = 10, quizLink = "https://quiz-maker.com/1", isActive = 'True')
        db.session.add(q1)
        db.session.commit()

        request_body = {
            "quizId": 1,
            "lessonId": 1,
            "isGraded": 1,
            "passingMark": 7,
            "numOfQns": 14,
            "quizLink": "https://quiz-maker.com/1",
            "isActive": 'False'
        }

        response = self.client.post("/quiz/update",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "data":{
                "quizId": 1,
                "lessonId": 1,
                "isGraded": 1,
                "passingMark": 7,
                "numOfQns": 14,
                "quizLink": "https://quiz-maker.com/1",
                "isActive": 'False'
            }
        })


if __name__ == '__main__':
    unittest.main()