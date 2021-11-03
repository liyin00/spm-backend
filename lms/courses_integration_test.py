import unittest
import flask_testing
import json
from datetime import datetime
from lms import app, db, Course

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


class TestCourses(TestApp):
    #test searching all courses
    def test_search_all_courses(self):
        c1 = Course(courseName = 'abc', courseDesc = '123',
                    prerequisites = "def", isActive = 1)
        c2 = Course(courseName = 'def', courseDesc = '456',
                    prerequisites = "ghi", isActive = 0)
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        response = self.client.get('/courses')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data':{
                "courses": [
                    {
                        "courseDesc": "123",
                        "courseId": 1,
                        "courseName": "abc",
                        "isActive": 1,
                        "prerequisites": "def"
                    },
                    {
                        "courseDesc": "456",
                        "courseId": 2,
                        "courseName": "def",
                        "isActive": 0,
                        "prerequisites": "ghi"
                    }
                ]
            }
        })

    #test search courses if database is empty
    def test_search_empty_courses(self):
        response = self.client.get('/courses')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "There is no available course information."
        })

    #test search course by name
    def test_search_course_by_courseName(self):
        c1 = Course(courseName = 'abc', courseDesc = '123',
                    prerequisites = "def", isActive = 1)
        db.session.add(c1)
        db.session.commit()

        response = self.client.get("/course/abc")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data':{
                "courseDesc": "123",
                "courseId": 1,
                "courseName": "abc",
                "isActive": 1,
                "prerequisites": "def"
            }
        })

    #test search invalid course name
    def test_search_course_by_invalid_courseName(self):
        c1 = Course(courseName = 'abc', courseDesc = '123',
                    prerequisites = "def", isActive = 1)
        db.session.add(c1)
        db.session.commit()

        response = self.client.get("/course/abcd")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "Course Info not found."
        })

    #test add course
    def test_add_course(self):

        request_body = {
            "courseName": 'abc',
            "courseDesc": '123',
            "prerequisites": "def",
            "isActive": 1
        }

        response = self.client.post("/course/add",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "data":{
                "courseId": 1,
                "courseName": 'abc',
                "courseDesc": '123',
                "prerequisites": "def",
                "isActive": 1
            }
        })

    #test add a course which already exists course
    def test_add_existing_course(self):
        c1 = Course(courseName = 'abc', courseDesc = '123',
                    prerequisites = "def", isActive = 1)
        db.session.add(c1)
        db.session.commit()

        request_body = {
            "courseName": 'abc',
            "courseDesc": '123',
            "prerequisites": "def",
            "isActive": 1
        }

        response = self.client.post("/course/add",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There is an existing course with the same name."
        })

    #test delete a course by courseId
    def test_delete_existing_course(self):
        c1 = Course(courseId = 1, courseName = 'abc', courseDesc = '123',
                    prerequisites = "def", isActive = 1)
        db.session.add(c1)
        db.session.commit()

        response = self.client.post("/course/delete/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Course was successfully deleted."
        })

    #test delete a course that does not exist
    def test_delete_nonexisting_course(self):
        c1 = Course(courseId = 1, courseName = 'abc', courseDesc = '123',
                    prerequisites = "def", isActive = 1)
        db.session.add(c1)
        db.session.commit()

        response = self.client.post("/course/delete/2")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "Course was not found."
        })

    #test editing an existing course
    def test_edit_course(self):
        c1 = Course(courseName = 'abc', courseDesc = '123',
                    prerequisites = "def", isActive = 1)
        db.session.add(c1)
        db.session.commit()

        request_body = {
            "courseId": 1,
            "courseName": 'cab',
            "courseDesc": '321',
            "prerequisites": "fed",
            "isActive": 0
        }

        response = self.client.post("/course/update",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "data":{
                "courseId": 1,
                "courseName": 'cab',
                "courseDesc": '321',
                "prerequisites": "fed",
                "isActive": 0
            }
        })

    #test editing an non-existing course
    def test_edit_nonexistent_course(self):

        request_body = {
            "courseId": 1,
            "courseName": 'abc',
            "courseDesc": '321',
            "prerequisites": "fed",
            "isActive": 0
        }

        response = self.client.post("/course/update",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "This course does not exist."
        })


if __name__ == '__main__':
    unittest.main()