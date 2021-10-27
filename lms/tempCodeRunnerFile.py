    #test add new learner to class
    def test_add_new_learner(self):
        cc1 = CourseClass(courseClassId = 1, courseId = 1, startDateTime = datetime(2021, 10, 8), 
                            endDateTime = datetime(2021, 10, 9), learnerIds = {'a': 1, 'b': 0, 'c': 1},
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