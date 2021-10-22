import unittest
import flask_testing
import json
from datetime import datetime
from lms import app, db, Lesson

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

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
                    lessonContent = {'a': 1, 'b': 0, 'c': 1}, links = {'a': 1, 'b': 0, 'c': 1})
        l2 = Lesson(courseClassId = 1, lessonName = 'bac',
                    lessonContent = {'a': 1, 'b': 0, 'c': 1}, links = {'a': 1, 'b': 0, 'c': 1})
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
                        "lessonContent": {'a': 1, 'b': 0, 'c': 1}, 
                        "links": {'a': 1, 'b': 0, 'c': 1}
                    },
                    {
                        "lessonId": 2,
                        "courseClassId": 1, 
                        "lessonName": 'bac', 
                        "lessonContent": {'a': 1, 'b': 0, 'c': 1}, 
                        "links": {'a': 1, 'b': 0, 'c': 1} 
                    }
                ]
            }
        })

    #test search invalid course name
    def test_search_course_by_invalid_courseName(self):
        l1 = Lesson(courseClassId = 1, lessonName = 'abc',
                    lessonContent = {'a': 1, 'b': 0, 'c': 1}, links = {'a': 1, 'b': 0, 'c': 1})
        l2 = Lesson(courseClassId = 1, lessonName = 'bac',
                    lessonContent = {'a': 1, 'b': 0, 'c': 1}, links = {'a': 1, 'b': 0, 'c': 1})
        db.session.add(l1)
        db.session.add(l2)
        db.session.commit()

        response = self.client.get("/lessons/2")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "Lessons for this course class cannot be found."
        })


if __name__ == '__main__':
    unittest.main()