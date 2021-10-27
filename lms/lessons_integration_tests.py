import unittest
from flask.globals import request
import flask_testing
import json
from datetime import datetime
from lms import app, db, Lesson, CourseClass

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


class TestLessons(TestApp):
    #test search lessons by courseClassId
    def test_search_lessons_by_courseClassId(self):
        l1 = Lesson(courseClassId = 1, lessonName = 'abc',
                    lessonContent = "abc||123||lol", links = "www.google.com www.googledrive.com")
        l2 = Lesson(courseClassId = 1, lessonName = 'bac')
        db.session.add(l1)
        db.session.add(l2)
        db.session.commit()

        response = self.client.get("/lessons/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data':{
                "lessons":[
                    {
                        "lessonId": 1,
                        "courseClassId": 1, 
                        "lessonName": 'abc', 
                        "lessonContent": ["abc", "123", "lol"], 
                        "links": ["www.google.com", "www.googledrive.com"]
                    },
                    {
                        "lessonId": 2,
                        "courseClassId": 1, 
                        "lessonName": 'bac', 
                        "lessonContent": None, 
                        "links": None 
                    }
                ]
            }
        })

    #test search invalid courseclassId
    def test_search_lesson_by_invalid_courseClassId(self):
        l1 = Lesson(courseClassId = 1, lessonName = 'abc',
                    lessonContent = "abc||123||lol", links = "www.google.com www.googledrive.com")
        l2 = Lesson(courseClassId = 1, lessonName = 'bac')
        db.session.add(l1)
        db.session.add(l2)
        db.session.commit()

        response = self.client.get("/lessons/2")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "Lessons for this course class cannot be found."
        })

    #test add lesson
    def test_add_lesson(self):
        cc1 = CourseClass(courseId = 1, startDateTime = datetime(2021, 10, 8), 
                            endDateTime = datetime(2021, 10, 9), learnerIds = "{'a': 1, 'b': 0, 'c': 1}",
                            trainerId = 1, classSize = 10)
        db.session.add(cc1)
        db.session.commit()

        request_body = {
            "courseClassId": 1, 
            "lessonName": 'abc', 
            "lessonContent": ["abc", "123", "lol"], 
            "links": ["www.google.com", "www.googledrive.com"]
        }

        response = self.client.post("/lesson/add",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            'data':{
                "lessonId": 1,
                "courseClassId": 1, 
                "lessonName": 'abc', 
                "lessonContent": ["abc", "123", "lol"], 
                "links": ["www.google.com", "www.googledrive.com"]
                }
        })

    #test add lesson when courseclass do no exist
    def test_add_lesson_no_class(self):
        cc1 = CourseClass(courseId = 1, startDateTime = datetime(2021, 10, 8), 
                            endDateTime = datetime(2021, 10, 9), learnerIds = "{'a': 1, 'b': 0, 'c': 1}",
                            trainerId = 1, classSize = 10)
        db.session.add(cc1)
        db.session.commit()

        request_body = {
            "courseClassId": 2, #wrong courseClassId
            "lessonName": 'abc', 
            "lessonContent": ["abc", "123", "lol"], 
            "links": ["www.google.com", "www.googledrive.com"]
        }

        response = self.client.post("/lesson/add",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "This class does not exist."
        })

    #test delete lesson by lessonId
    def test_delete_existing_lesson(self):
        l1 = Lesson(courseClassId = 1, lessonName = 'abc',
                    lessonContent = "abc||123||lol", links = "www.google.com www.googledrive.com")
        l2 = Lesson(courseClassId = 1, lessonName = 'bac')
        db.session.add(l1)
        db.session.add(l2)
        db.session.commit()

        response = self.client.post("/lesson/delete/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Lesson was successfully deleted."
        })

    #test delete lesson that does not exist
    def test_delete_non_existing_lesson(self):
        l1 = Lesson(courseClassId = 1, lessonName = 'abc',
                    lessonContent = "abc||123||lol", links = "www.google.com www.googledrive.com")
        l2 = Lesson(courseClassId = 1, lessonName = 'bac')
        db.session.add(l1)
        db.session.add(l2)
        db.session.commit()

        response = self.client.post("/lesson/delete/3")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "Lesson was not found."
        })

if __name__ == '__main__':
    unittest.main()