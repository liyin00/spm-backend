import unittest
from flask.globals import request
import flask_testing
import json
from datetime import datetime
from lms import app, db, CourseClass, Course

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


class TestCourseClasses(TestApp):
    # #test searching classes by courseId
    # def test_searching_classes(self):
    #     cc1 = CourseClass(courseId = 1, startDateTime = datetime(2021, 10, 8), 
    #                         endDateTime = datetime(2021, 10, 9), learnerIds = "{'a': 1, 'b': 0, 'c': 1}",
    #                         trainerId = 1, classSize = 10)
    #     cc2 = CourseClass(courseId = 1)
    #     db.session.add(cc1)
    #     db.session.add(cc2)
    #     db.session.commit()

    #     response = self.client.get('/class/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json, {
    #         'data':{
    #             "classes": [
    #                 {
    #                     "classSize": 10,
    #                     "courseClassId": 1,
    #                     "courseId": 1,
    #                     "endDateTime": 'Sat, 09 Oct 2021 00:00:00 GMT',
    #                     "learnerIds": {'a': 1, 'b': 0, 'c': 1},
    #                     "startDateTime": 'Fri, 08 Oct 2021 00:00:00 GMT',
    #                     "trainerId": 1
    #                 },
    #                 {
    #                     "classSize": None,
    #                     "courseClassId": 2,
    #                     "courseId": 1,
    #                     "endDateTime": None,
    #                     "learnerIds": None,
    #                     "startDateTime": None,
    #                     "trainerId": None
    #                 }
    #             ]
    #         }
    #     })

#     #test searching non-existent classes by courseId
#     def test_searching_empty_classes(self):
#         cc1 = CourseClass(courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         cc2 = CourseClass(courseId = 1)
#         db.session.add(cc1)
#         db.session.add(cc2)
#         db.session.commit()

#         response = self.client.get('/class/2')
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json, {
#             'message': "Classes was not found."
#         })

#     #test add class
#     def test_add_class(self):
#         c1 = Course(courseId = 1, courseName = 'abc', courseDesc = '123',
#                     prerequisites = "def", isActive = 1)
#         db.session.add(c1)
#         db.session.commit()

#         request_body = {
#             "classSize": 10,
#             "courseId": 1,
#             "endDateTime": '09/10/2021',
#             "learnerIds": {'a': 1, 'b': 0, 'c': 1},
#             "startDateTime": '08/10/2021',
#             "trainerId": 1
#         }

#         response = self.client.post("/class/add",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json, {
#             "data":{
#                 "classSize": 10,
#                 "courseClassId": 1,
#                 "courseId": 1,
#                 "endDateTime": 'Sat, 09 Oct 2021 00:00:00 GMT',
#                 "learnerIds": {'a': 1, 'b': 0, 'c': 1},
#                 "startDateTime": 'Fri, 08 Oct 2021 00:00:00 GMT',
#                 "trainerId": 1
#             }
#         })

#     #test add class when course do not exist
#     def test_add_class_no_course(self):
#         c1 = Course(courseId = 1, courseName = 'abc', courseDesc = '123',
#                     prerequisites = "def", isActive = 1)
#         db.session.add(c1)
#         db.session.commit()

#         request_body = {
#             "classSize": 10,
#             "courseId": 2, #wrong courseId
#             "endDateTime": '09/10/2021',
#             "learnerIds": {'a': 1, 'b': 0, 'c': 1},
#             "startDateTime": '08/10/2021',
#             "trainerId": 1
#         }

#         response = self.client.post("/class/add",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json, {
#             "message": "This course does not exist."
#         })

#     #test delete class by courseClassId
#     def test_delete_existing_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         response = self.client.post("/class/delete/1")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {
#             "message": "Class was successfully deleted."
#         })

#     #test delete class that does not exist
#     def test_delete_nonexisting_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         response = self.client.post("/class/delete/2")
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json, {
#             "message": "Class was not found."
#         })

    #test add new learner to class
    def test_add_new_learner(self):
        cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
                            endDateTime = datetime(2021, 10, 9), learnerIds = "{'a': 1, 'b': 0, 'c': 1}",
                            trainerId = 1, classSize = 10)
        db.session.add(cc1)
        db.session.commit()

        request_body = {
            "courseClassId": 1,
            "learnerId": 'd'
        }

        response = self.client.post("/class/add/learner",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "data":{
                "classSize": 10,
                "courseClassId": 1,
                "courseId": 1,
                "endDateTime": 'Sat, 09 Oct 2021 00:00:00 GMT',
                "learnerIds": {'a': 1, 'b': 0, 'c': 1, 'd': 0},
                "startDateTime": 'Fri, 08 Oct 2021 00:00:00 GMT',
                "trainerId": 1
            }
        })

#     #test add learner to non-exising class
#     def test_add_learner_nonexisting_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 2,
#             "learnerId": 'd'
#         }

#         response = self.client.post("/class/add/learner",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json, {
#                 "message": "This class does not exist."
#         })

#     #test add existing learner to class
#     def test_add_learner_nonexisting_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 1,
#             "learnerId": 'a'
#         }

#         response = self.client.post("/class/add/learner",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#                 "message": "Learner is already in this class."
#         })

#     #test accept new learner to class
#     def test_accept_new_learner(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1, 'd': 0},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 1,
#             "learnerId": 'd'
#         }

#         response = self.client.post("/class/accept/learner",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json, {
#             "data":{
#                 "classSize": 10,
#                 "courseClassId": 1,
#                 "courseId": 1,
#                 "endDateTime": 'Sat, 09 Oct 2021 00:00:00 GMT',
#                 "learnerIds": {'a': 1, 'b': 0, 'c': 1, 'd': 1},
#                 "startDateTime": 'Fri, 08 Oct 2021 00:00:00 GMT',
#                 "trainerId": 1
#             }
#         })

#     #test accept learner to non-exising class
#     def test_accept_learner_nonexisting_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1, 'd': 0},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 2,
#             "learnerId": 'd'
#         }

#         response = self.client.post("/class/add/learner",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json, {
#                 "message": "This class does not exist."
#         })

#     #test add new trainer to class
#     def test_add_new_trainer(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 1,
#             "trainerId": 2
#         }

#         response = self.client.post("/class/add/trainer",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json, {
#             "data":{
#                 "classSize": 10,
#                 "courseClassId": 1,
#                 "courseId": 1,
#                 "endDateTime": 'Sat, 09 Oct 2021 00:00:00 GMT',
#                 "learnerIds": {'a': 1, 'b': 0, 'c': 1},
#                 "startDateTime": 'Fri, 08 Oct 2021 00:00:00 GMT',
#                 "trainerId": 2
#             }
#         })

#     #test add new trainer to non-existing class
#     def test_add_trainer_nonexisting_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 2,
#             "trainerId": 2
#         }

#         response = self.client.post("/class/add/trainer",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json, {
#             "message": "This class does not exist."
#         })

#     #test delete existing learner from class
#     def test_delete_learner_from_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 1,
#             "learnerId": 'a'
#         }

#         response = self.client.post("/class/delete/learner",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json, {
#             "data":{
#                 "classSize": 10,
#                 "courseClassId": 1,
#                 "courseId": 1,
#                 "endDateTime": 'Sat, 09 Oct 2021 00:00:00 GMT',
#                 "learnerIds": {'b': 0, 'c': 1},
#                 "startDateTime": 'Fri, 08 Oct 2021 00:00:00 GMT',
#                 "trainerId": 1
#             }
#         })

#     #test delete learner from non-existent class
#     def test_delete_learner_from_nonexistent_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 2,
#             "learnerId": 'a'
#         }

#         response = self.client.post("/class/delete/learner",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json, {
#             "message": "This class does not exist."
#         })

#     #test delete non-existent learner from class
#     def test_delete_nonexistent_learner_from_class(self):
#         cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
#                             endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
#                             trainerId = 1, classSize = 10)
#         db.session.add(cc1)
#         db.session.commit()

#         request_body = {
#             "courseClassId": 1,
#             "learnerId": 'd'
#         }

#         response = self.client.post("/class/delete/learner",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json, {
#             "message": "Learner is not in this class."
#         })

if __name__ == '__main__':
    unittest.main()