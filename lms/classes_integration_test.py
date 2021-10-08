import unittest
import flask_testing
import json
from lms import app, db, CourseClass

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


class TestCourseClasses(TestApp):
    #test searching classes by courseId
    def test_searching_classes(self):
        cc1 = CourseClass(courseId = '1')
        cc2 = CourseClass(courseId = '1')
        db.session.add(cc1)
        db.session.add(cc2)
        db.session.commit()

        response = self.client.get('/courseclass/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data':{
                "classes": [
                    {
                        "classSize": None,
                        "courseClassId": 1,
                        "courseId": 1,
                        "endDateTime": None,
                        "learnerId": None,
                        "startDateTime": None,
                        "trainerId": None
                    },
                    {
                        "classSize": None,
                        "courseClassId": 2,
                        "courseId": 1,
                        "endDateTime": None,
                        "learnerId": None,
                        "startDateTime": None,
                        "trainerId": None
                    }
                ]
            }
        })

    #test searching non-existent classes by courseId
    def test_searching_empty_classes(self):
        cc1 = CourseClass(courseId = '1')
        cc2 = CourseClass(courseId = '1')
        db.session.add(cc1)
        db.session.add(cc2)
        db.session.commit()

        response = self.client.get('/courseclass/2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            'message': "Classes was not found."
        })

if __name__ == '__main__':
    unittest.main()