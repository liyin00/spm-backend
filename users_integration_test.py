"""
Owner of TDD: Jeremy
"""

import unittest
import flask_testing
import json
from datetime import datetime
from lms import app, db, User

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


class TestUsers(TestApp):
    #test get all users
    def test_get_all_users(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        test_user2 = User(name = 'testuser2', subrole = 'testsubrole2',
                    department = "testdepartment2", email = "testuser2@email.com")
        db.session.add(test_user1)
        db.session.add(test_user2)
        db.session.commit()

        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data':{
                "users": [
                    {
                        "name": "testuser1",
                        "subrole": "testsubrole1",
                        "department": "testdepartment1",
                        "email": "testuser1@email.com",
                        "userId": 1
                    },
                    {
                        "name": "testuser2",
                        "subrole": "testsubrole2",
                        "department": "testdepartment2",
                        "email": "testuser2@email.com",
                        "userId": 2
                    },
                ]
            }
        })

    #test get all users when database is empty
    def test_get_all_users_empty(self):
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "There are no available users."
        })

    #test get user by name
    def test_get_user_by_name(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        response = self.client.get("/user/name/testuser1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data':{
                "name": "testuser1",
                "subrole": "testsubrole1",
                "department": "testdepartment1",
                "email": "testuser1@email.com",
                "userId": 1
            },
        })

    #test get user by name if user name does not exist in database
    def test_get_user_by_name_invalid(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        response = self.client.get("/user/name/testuser0")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "User not found."
        })

    #test get user by userId
    def test_get_user_by_userId(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        response = self.client.get("/user/id/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data':{
                "name": "testuser1",
                "subrole": "testsubrole1",
                "department": "testdepartment1",
                "email": "testuser1@email.com",
                "userId": 1
            },
        })

    #test search invalid user name
    def test_get_user_by_userId_invalid(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        response = self.client.get("/user/id/2")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "User not found."
        })

    #test create user
    def test_create_user(self):

        request_body = {
            "name": 'testuser1',
            "subrole": 'testsubrole',
            "department": "testdepartment",
            "email": "testuser1@email.com"
        }

        response = self.client.post("/user",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "data":{
                "userId": 1,
                "name": 'testuser1',
                "subrole": 'testsubrole',
                "department": "testdepartment",
                "email": "testuser1@email.com"
            }
        })

    #test add user whose name already exists
    def test_create_user_invalid(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        request_body = {
            "name": 'testuser1',
            "subrole": 'testsubrole',
            "department": "testdepartment",
            "email": "testuser1@email.com"
        }

        response = self.client.post("/user",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There is an existing user with the same name."
        })

    #test delete a user by userId
    def test_delete_user(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        response = self.client.delete("/user/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "User was successfully deleted."
        })

    #test delete a user by userId that does not exist
    def test_delete_user_invalid(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        response = self.client.delete("/user/2")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "User was not found."
        })

    #test update a user
    def test_update_uesr_by_userId(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        request_body = {
            "userId": 1,
            "name": 'updated_testuser1',
            "subrole": 'updated_testsubrole',
            "department": "updated_testdepartment",
            "email": "updated_testuser1@email.com"
        }

        response = self.client.patch("/user",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "data":{
                "userId": 1,
                "name": 'updated_testuser1',
                "subrole": 'updated_testsubrole',
                "department": "updated_testdepartment",
                "email": "updated_testuser1@email.com"
            }
        })

    #test update a user that does not exist
    def test_update_uesr_by_userId_invalid(self):
        test_user1 = User(name = 'testuser1', subrole = 'testsubrole1',
                    department = "testdepartment1", email = "testuser1@email.com")
        db.session.add(test_user1)
        db.session.commit()

        request_body = {
            "userId": 2,
            "name": 'updated_testuser1',
            "subrole": 'updated_testsubrole',
            "department": "updated_testdepartment",
            "email": "updated_testuser1@email.com"
        }

        response = self.client.patch("/user",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "This user does not exist."
        })


    #test get user by name
    def test_get_engineers_by_name(self):
        test_engineer1 = User(name = 'testengineer1', subrole = 'testsubrole1',
                    department = "Engineer", email = "testengineer1@email.com")
        db.session.add(test_engineer1)
        db.session.commit()

        response = self.client.get("/user/engineer/name/testengineer1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': [
                {
                    "name": "testengineer1",
                    "subrole": "testsubrole1",
                    "department": "Engineer",
                    "email": "testengineer1@email.com",
                    "userId": 1
                }
            ]
        })

    #test get user by name if user name does not exist in database
    def test_get_engineers_by_name_invalid(self):
        test_engineer1 = User(name = 'testengineer1', subrole = 'testsubrole1',
                    department = "Engineer", email = "testengineer1@email.com")
        db.session.add(test_engineer1)
        db.session.commit()

        response = self.client.get("/user/engineer/name/testengineer0")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "message": "Engineer not found."
        })

if __name__ == '__main__':
    unittest.main()